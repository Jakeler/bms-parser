/**
 * Copyright 2015-2019 Kaitai Project: MIT license
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package io.kaitai.struct;

import java.io.ByteArrayOutputStream;
import java.io.Closeable;
import java.io.IOException;
import java.util.Arrays;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

/**
 * KaitaiStream provides implementation of
 * <a href="https://github.com/kaitai-io/kaitai_struct/wiki/Kaitai-Struct-stream-API">Kaitai Struct stream API</a>
 * for Java.
 *
 * It provides a wide variety of simple methods to read (parse) binary
 * representations of primitive types, such as integer and floating
 * point numbers, byte arrays and strings, and also provides stream
 * positioning / navigation methods with unified cross-language and
 * cross-toolkit semantics.
 *
 * This is abstract class, which serves as an interface description and
 * a few default method implementations, which are believed to be common
 * for all (or at least most) implementations. Different implementations
 * of this interface may provide way to parse data from local files,
 * in-memory buffers or arrays, remote files, network streams, etc.
 *
 * Typically, end users won't access any of these Kaitai Stream classes
 * manually, but would describe a binary structure format using .ksy language
 * and then would use Kaitai Struct compiler to generate source code in
 * desired target language.  That code, in turn, would use this class
 * and API to do the actual parsing job.
 */
public abstract class KaitaiStream implements Closeable {
    protected int bitsLeft = 0;
    protected long bits = 0;

    @Override
    abstract public void close() throws IOException;

    //region Stream positioning

    /**
     * Check if stream pointer is at the end of stream.
     * @return true if we are located at the end of the stream
     */
    abstract public boolean isEof();

    /**
     * Set stream pointer to designated position (int).
     * @param newPos new position (offset in bytes from the beginning of the stream)
     */
    abstract public void seek(int newPos);

    /**
     * Set stream pointer to designated position (long).
     * @param newPos new position (offset in bytes from the beginning of the stream)
     */
    abstract public void seek(long newPos);

    /**
     * Get current position of a stream pointer.
     * @return pointer position, number of bytes from the beginning of the stream
     */
    abstract public int pos();

    /**
     * Get total size of the stream in bytes.
     * @return size of the stream in bytes
     */
    abstract public long size();

    //endregion

    //region Integer numbers

    //region Signed

    /**
     * Reads one signed 1-byte integer, returning it properly as Java's "byte" type.
     * @return 1-byte integer read from a stream
     */
    abstract public byte readS1();

    //region Big-endian

    abstract public short readS2be();
    abstract public int readS4be();
    abstract public long readS8be();

    //endregion

    //region Little-endian

    abstract public short readS2le();
    abstract public int readS4le();
    abstract public long readS8le();

    //endregion

    //endregion

    //region Unsigned

    abstract public int readU1();

    //region Big-endian

    abstract public int readU2be();

    abstract public long readU4be();

    /**
     * Reads one unsigned 8-byte integer in big-endian encoding. As Java does not
     * have a primitive data type to accomodate it, we just reuse {@link #readS8be()}.
     * @return 8-byte signed integer (pretending to be unsigned) read from a stream
     */
    public long readU8be() {
        return readS8be();
    }

    //endregion

    //region Little-endian

    abstract public int readU2le();

    abstract public long readU4le();

    /**
     * Reads one unsigned 8-byte integer in little-endian encoding. As Java does not
     * have a primitive data type to accomodate it, we just reuse {@link #readS8le()}.
     * @return 8-byte signed integer (pretending to be unsigned) read from a stream
     */
    public long readU8le() {
        return readS8le();
    }

    //endregion

    //endregion

    //endregion

    //region Floating point numbers

    //region Big-endian

    abstract public float readF4be();
    abstract public double readF8be();

    //endregion

    //region Little-endian

    abstract public float readF4le();
    abstract public double readF8le();

    //endregion

    //endregion

    //region Unaligned bit values

    public void alignToByte() {
        bits = 0;
        bitsLeft = 0;
    }

    public long readBitsInt(int n) {
        int bitsNeeded = n - bitsLeft;
        if (bitsNeeded > 0) {
            // 1 bit  => 1 byte
            // 8 bits => 1 byte
            // 9 bits => 2 bytes
            int bytesNeeded = ((bitsNeeded - 1) / 8) + 1;
            byte[] buf = readBytes(bytesNeeded);
            for (byte b : buf) {
                bits <<= 8;
                // b is signed byte, convert to unsigned using "& 0xff" trick
                bits |= (b & 0xff);
                bitsLeft += 8;
            }
        }

        // raw mask with required number of 1s, starting from lowest bit
        long mask = getMaskOnes(n);
        // shift mask to align with highest bits available in "bits"
        int shiftBits = bitsLeft - n;
        mask <<= shiftBits;
        // derive reading result
        long res = (bits & mask) >>> shiftBits;
        // clear top bits that we've just read => AND with 1s
        bitsLeft -= n;
        mask = getMaskOnes(bitsLeft);
        bits &= mask;

        return res;
    }

    private static long getMaskOnes(int n) {
        if (n == 64) {
            return 0xffffffffffffffffL;
        } else {
            return (1L << n) - 1;
        }
    }

    //endregion

    //region Byte arrays

    /**
     * Reads designated number of bytes from the stream.
     * @param n number of bytes to read
     * @return read bytes as byte array
     */
    abstract public byte[] readBytes(long n);

    /**
     * Reads all the remaining bytes in a stream as byte array.
     * @return all remaining bytes in a stream as byte array
     */
    abstract public byte[] readBytesFull();

    abstract public byte[] readBytesTerm(int term, boolean includeTerm, boolean consumeTerm, boolean eosError);

    /**
     * Checks that next bytes in the stream match match expected fixed byte array.
     * It does so by determining number of bytes to compare, reading them, and doing
     * the actual comparison. If they differ, throws a {@link UnexpectedDataError}
     * runtime exception.
     * @param expected contents to be expected
     * @return read bytes as byte array, which are guaranteed to equal to expected
     * @throws UnexpectedDataError if read data from stream isn't equal to given data
     */
    public byte[] ensureFixedContents(byte[] expected) {
        byte[] actual = readBytes(expected.length);
        if (!Arrays.equals(actual, expected))
            throw new UnexpectedDataError(actual, expected);
        return actual;
    }

    public static byte[] bytesStripRight(byte[] bytes, byte padByte) {
        int newLen = bytes.length;
        while (newLen > 0 && bytes[newLen - 1] == padByte)
            newLen--;
        return Arrays.copyOf(bytes, newLen);
    }

    public static byte[] bytesTerminate(byte[] bytes, byte term, boolean includeTerm) {
        int newLen = 0;
        int maxLen = bytes.length;
        while (bytes[newLen] != term && newLen < maxLen)
            newLen++;
        if (includeTerm && newLen < maxLen)
            newLen++;
        return Arrays.copyOf(bytes, newLen);
    }

    /**
     * Checks if supplied number of bytes is a valid number of elements for Java
     * byte array: converts it to int, if it is, or throws an exception if it is not.
     * @param n number of bytes for byte array as long
     * @return number of bytes, converted to int
     */
    protected int toByteArrayLength(long n) {
        if (n > Integer.MAX_VALUE) {
            throw new IllegalArgumentException(
                    "Java byte arrays can be indexed only up to 31 bits, but " + n + " size was requested"
            );
        }
        if (n < 0) {
            throw new IllegalArgumentException(
                    "Byte array size can't be negative, but " + n + " size was requested"
            );
        }
        return (int) n;
    }

    //endregion

    //region Byte array processing

    /**
     * Performs a XOR processing with given data, XORing every byte of input with a single
     * given value.
     * @param data data to process
     * @param key value to XOR with
     * @return processed data
     */
    public static byte[] processXor(byte[] data, int key) {
        int dataLen = data.length;
        byte[] r = new byte[dataLen];
        for (int i = 0; i < dataLen; i++)
            r[i] = (byte) (data[i] ^ key);
        return r;
    }

    /**
     * Performs a XOR processing with given data, XORing every byte of input with a key
     * array, repeating key array many times, if necessary (i.e. if data array is longer
     * than key array).
     * @param data data to process
     * @param key array of bytes to XOR with
     * @return processed data
     */
    public static byte[] processXor(byte[] data, byte[] key) {
        int dataLen = data.length;
        int valueLen = key.length;

        byte[] r = new byte[dataLen];
        int j = 0;
        for (int i = 0; i < dataLen; i++) {
            r[i] = (byte) (data[i] ^ key[j]);
            j = (j + 1) % valueLen;
        }
        return r;
    }

    /**
     * Performs a circular left rotation shift for a given buffer by a given amount of bits,
     * using groups of groupSize bytes each time. Right circular rotation should be performed
     * using this procedure with corrected amount.
     * @param data source data to process
     * @param amount number of bits to shift by
     * @param groupSize number of bytes per group to shift
     * @return copy of source array with requested shift applied
     */
    public static byte[] processRotateLeft(byte[] data, int amount, int groupSize) {
        byte[] r = new byte[data.length];
        switch (groupSize) {
            case 1:
                for (int i = 0; i < data.length; i++) {
                    byte bits = data[i];
                    // http://stackoverflow.com/a/19181827/487064
                    r[i] = (byte) (((bits & 0xff) << amount) | ((bits & 0xff) >>> (8 - amount)));
                }
                break;
            default:
                throw new UnsupportedOperationException("unable to rotate group of " + groupSize + " bytes yet");
        }
        return r;
    }

    private final static int ZLIB_BUF_SIZE = 4096;

    /**
     * Performs an unpacking ("inflation") of zlib-compressed data with usual zlib headers.
     * @param data data to unpack
     * @return unpacked data
     * @throws RuntimeException if data can't be decoded
     */
    public static byte[] processZlib(byte[] data) {
        Inflater ifl = new Inflater();
        ifl.setInput(data);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte buf[] = new byte[ZLIB_BUF_SIZE];
        while (!ifl.finished()) {
            try {
                int decBytes = ifl.inflate(buf);
                baos.write(buf, 0, decBytes);
            } catch (DataFormatException e) {
                throw new RuntimeException(e);
            }
        }
        ifl.end();
        return baos.toByteArray();
    }

    //endregion

    //region Misc runtime operations

    /**
     * Performs modulo operation between two integers: dividend `a`
     * and divisor `b`. Divisor `b` is expected to be positive. The
     * result is always 0 &lt;= x &lt;= b - 1.
     * @param a dividend
     * @param b divisor
     * @return result
     */
    public static int mod(int a, int b) {
        if (b <= 0)
            throw new ArithmeticException("mod divisor <= 0");
        int r = a % b;
        if (r < 0)
            r += b;
        return r;
    }

    /**
     * Performs modulo operation between two integers: dividend `a`
     * and divisor `b`. Divisor `b` is expected to be positive. The
     * result is always 0 &lt;= x &lt;= b - 1.
     * @param a dividend
     * @param b divisor
     * @return result
     */
    public static long mod(long a, long b) {
        if (b <= 0)
            throw new ArithmeticException("mod divisor <= 0");
        long r = a % b;
        if (r < 0)
            r += b;
        return r;
    }

    /**
     * Compares two byte arrays in lexicographical order. Makes extra effort
     * to compare bytes properly, as *unsigned* bytes, i.e. [0x90] would be
     * greater than [0x10].
     * @param a first byte array to compare
     * @param b second byte array to compare
     * @return negative number if a &lt; b, 0 if a == b, positive number if a &gt; b
     * @see Comparable#compareTo(Object)
     */
    public static int byteArrayCompare(byte[] a, byte[] b) {
        if (a == b)
            return 0;
        int al = a.length;
        int bl = b.length;
        int minLen = Math.min(al, bl);
        for (int i = 0; i < minLen; i++) {
            int cmp = (a[i] & 0xff) - (b[i] & 0xff);
            if (cmp != 0)
                return cmp;
        }

        // Reached the end of at least one of the arrays
        if (al == bl) {
            return 0;
        } else {
            return al - bl;
        }
    }

    /**
     * Finds the minimal byte in a byte array, treating bytes as
     * unsigned values.
     * @param b byte array to scan
     * @return minimal byte in byte array as integer
     */
    public static int byteArrayMin(byte[] b) {
        int min = Integer.MAX_VALUE;
        for (int i = 0; i < b.length; i++) {
            int value = b[i] & 0xff;
            if (value < min)
                min = value;
        }
        return min;
    }

    /**
     * Finds the maximal byte in a byte array, treating bytes as
     * unsigned values.
     * @param b byte array to scan
     * @return maximal byte in byte array as integer
     */
    public static int byteArrayMax(byte[] b) {
        int max = 0;
        for (int i = 0; i < b.length; i++) {
            int value = b[i] & 0xff;
            if (value > max)
                max = value;
        }
        return max;
    }

    //endregion

    /**
     * Exception class for an error that occurs when some fixed content
     * was expected to appear, but actual data read was different.
     */
    public static class UnexpectedDataError extends RuntimeException {
        public UnexpectedDataError(byte[] actual, byte[] expected) {
            super(
                    "Unexpected fixed contents: got " + byteArrayToHex(actual) +
                    ", was waiting for " + byteArrayToHex(expected)
            );
        }

        private static String byteArrayToHex(byte[] arr) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < arr.length; i++) {
                if (i > 0)
                    sb.append(' ');
                sb.append(String.format("%02x", arr[i]));
            }
            return sb.toString();
        }
    }

    /**
     * Error that occurs when default endianness should be decided with a
     * switch, but nothing matches (although using endianness expression
     * implies that there should be some positive result).
     */
    public static class UndecidedEndiannessError extends RuntimeException {}

    /**
     * Common ancestor for all error originating from Kaitai Struct usage.
     * Stores KSY source path, pointing to an element supposedly guilty of
     * an error.
     */
    public static class KaitaiStructError extends RuntimeException {
        public KaitaiStructError(String msg, String srcPath) {
            super(srcPath + ": " + msg);
            this.srcPath = srcPath;
        }

        protected String srcPath;
    }

    /**
     * Common ancestor for all validation failures. Stores pointer to
     * KaitaiStream IO object which was involved in an error.
     */
    public static class ValidationFailedError extends KaitaiStructError {
        public ValidationFailedError(String msg, KaitaiStream io, String srcPath) {
            super("at pos " + io.pos() + ": validation failed: " + msg, srcPath);
            this.io = io;
        }

        protected KaitaiStream io;

        protected static String byteArrayToHex(byte[] arr) {
            StringBuilder sb = new StringBuilder("[");
            for (int i = 0; i < arr.length; i++) {
                if (i > 0)
                    sb.append(' ');
                sb.append(String.format("%02x", arr[i]));
            }
            sb.append(']');
            return sb.toString();
        }
    }

    /**
     * Signals validation failure: we required "actual" value to be equal to
     * "expected", but it turned out that it's not.
     */
    public static class ValidationNotEqualError extends ValidationFailedError {
        public ValidationNotEqualError(byte[] expected, byte[] actual, KaitaiStream io, String srcPath) {
            super("not equal, expected " + byteArrayToHex(expected) + ", but got " + byteArrayToHex(actual), io, srcPath);
        }

        public ValidationNotEqualError(Object expected, Object actual, KaitaiStream io, String srcPath) {
            super("not equal, expected " + expected + ", but got " + actual, io, srcPath);
        }

        protected Object expected;
        protected Object actual;
    }
}
