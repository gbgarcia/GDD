using System;
using System.IO;

namespace circuloConAlpha
{
    class Program
    {
        static byte[,] alphas;

        static void Main(string[] args)
        {
            BinaryWriter bw = new BinaryWriter(new FileStream(@"c:\desktop\circulo.bmpx", FileMode.Create));

			// http://en.wikipedia.org/wiki/BMP_file_format#Example_2
			
            // header: BMP de 32bits con alpha, de 1600x460
            byte[] header = {
	            0x42, 0x4D, 0x7A, 0xEC, 0x2C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7A, 0x00,
	            0x00, 0x00, 0x6C, 0x00, 0x00, 0x00, 0x40, 0x06, 0x00, 0x00, 0xCC, 0x01,
	            0x00, 0x00, 0x01, 0x00, 0x20, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0xEC,
	            0x2C, 0x00, 0x13, 0x0B, 0x00, 0x00, 0x13, 0x0B, 0x00, 0x00, 0x00, 0x00,
	            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF,
	            0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x20, 0x6E,
	            0x69, 0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	            0x00, 0x00
            };

            bw.Write(header);

            alphas = new byte[1600, 460];
            for (int x = 0; x < 1600; x++)
            {
                for (int y = 0; y < 460; y++)
                {
                    alphas[x, y] = 170;     // semi-transparente
                }
            }


            const int x0 = 799;     // centro del circulo
            const int y0 = 437;

            const int r1=50;        // radio de transparente

            for (int x = -r1; x <= r1; x++)
            {
                for (int y = -r1; y <= r1; y++)
                {
                    if (x * x + y * y <= r1 * r1 + r1 * 0.8f && y0 + y < 460)
                    {
                        alphas[x0 + x, y0 + y] = 0;
                    }
                }
            }

            const int r2 = 65;      // radio de degradado

            for (int x = -r2; x <= r2; x++)
            {
                for (int y = -r2; y <= r2; y++)
                {
                    if (x * x + y * y <= r2 * r2 + r2 * 0.8f
                        && x * x + y * y > r1 * r1 + r1 * 0.8f
                        && y0 + y < 460)
                    {
                        alphas[x0 + x, y0 + y] = (byte)(Math.Pow(((Math.Sqrt(x * x + y * y) - r1) / ((float)(r2 - r1))),2) * 170);  // al cuadrado
                    }
                }
            }

            for (int y = 459; y >= 0; y--)
            {
                for (int x = 0; x < 1600; x++)
                {
                    bw.Write((byte)0);  //
                    bw.Write((byte)0);  // negro
                    bw.Write((byte)0);  //
                    bw.Write(alphas[x, y]);     // alpha
                }
            }

            bw.Close();
        }
    }
}
