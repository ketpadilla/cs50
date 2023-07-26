#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: copy infule outfile\n");
        return 1;
    }

    // Open input file for reading
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "rb");
    if (inptr == NULL)
    {
        printf("Could not open file %s.\n", infile);
        return 2;
    }

    // Read header
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, inptr);

    // Use check_format to ensure WAV format
    if (check_format(header) == 0)
    {
        printf("Not a Wave File\n");
        return 1;
    }

    if (header.audioFormat != 1)
    {
        printf("Not a Wave File\n");
        return 1;
    }

    // Open output file for writing
    char *outfile = argv[2];
    FILE *outptr = fopen(outfile, "wb");
    if (outptr == NULL)
    {
        printf("Could not open file %s.\n", outfile);
        return 1;
    }

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, outptr);

    // Use get_block_size to calculate size of block
    int size = get_block_size(header);

    // Write reversed audio to file
    if (fseek(inptr, size, SEEK_END))
    {
        return 1;
    }

    BYTE buffer[size];
    while (ftell(inptr) - size > sizeof(header))
    {
        if (fseek(inptr, - 2 * size, SEEK_CUR))
        {
            return 1;
        }

        fread(buffer, size, 1, inptr);
        fwrite(buffer, size, 1, outptr);
    }

    fclose(outptr);
    fclose(inptr);
}

int check_format(WAVHEADER header)
{
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 1;
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    int size = header.numChannels * header.bitsPerSample / 8;
    return size;
}