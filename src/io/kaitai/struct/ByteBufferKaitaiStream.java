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
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

/**
 * An implementation of {@link KaitaiStream} backed by a {@link ByteBuffer}.
 * It can be either a {@link MappedByteBuffer} backed by {@link FileChannel},
 * or a regular wrapper over a given byte array).
 */
public class ByteBufferKaitaiStream extends KaitaiStream {
    private FileChannel fc;
    private ByteBuffer bb;

    /**
     * Initializes a stream, reading from a local file with specified fileName.
     * Internally, FileChannel + MappedByteBuffer will be used.
     * @param fileName file to read
     * @throws IOException if file can't be read
     */
    public ByteBufferKaitaiStream(String fileName) throws IOException {
        fc = FileChannel.open(Paths.get(fileName), StandardOpenOption.READ);
        bb = fc.map(FileChannel.MapMode.READ_ONLY, 0, fc.size());
    }

    /**
     * Initializes a stream that will get data from given byte array when read.
     * Internally, ByteBuffer wrapping given array will be used.
     * @param arr byte array to read
     */
    public ByteBufferKaitaiStream(byte[] arr) {
        fc = null;
        bb = ByteBuffer.wrap(arr);
    }

    /**
     * Initializes a stream that will get data from given ByteBuffer when read.
     * @param buffer ByteBuffer to read
     */
    public ByteBufferKaitaiStream(ByteBuffer buffer) {
        fc = null;
        bb = buffer;
    }

    /**
     * Provide a read-only version of the {@link ByteBuffer} backing the data of this instance.
     * <p>
     * This way one can access the underlying raw bytes associated with this structure, but it is
     * important to note that the caller needs to know what this raw data is: Depending on the
     * hierarchy of user types, how the format has been described and how a user type is actually
     * used, it might be that one accesses all data of some format or only a special substream
     * view of it. We can't know currently, so one needs to keep that in mind when authoring a KSY
     * and e.g. use substreams with user types whenever such a type most likely needs to access its
     * underlying raw data. Using a substream in KSY and directly passing some raw data to a user
     * type outside of normal KS parse order is equivalent and will provide the same results. If no
     * substream is used instead, the here provided data might differ depending on the context in
     * which the associated type was parsed, because the underlying {@link ByteBuffer} might
     * contain the data of all parent types and such as well and not only the one the caller is
     * actually interested in.
     * </p>
     * <p>
     * The returned {@link ByteBuffer} is always rewinded to position 0, because this stream was
     * most likely used to parse a type already, in which case the former position would have been
     * at the end of the buffer. Such a position doesn't help a common reading user much and that
     * fact can easily be forgotten, repositioning to another index than the start is pretty easy
     * as well. Rewinding/repositioning doesn't even harm performance in any way.
     * </p>
     * @return read-only {@link ByteBuffer} to access raw data for the associated type.
     */
    public ByteBuffer asRoBuffer() {
        ByteBuffer retVal = this.bb.asReadOnlyBuffer();
        retVal.rewind();

        return retVal;
    }

    /**
     * Closes the stream safely. If there was an open file associated with it, closes that file.
     * For streams that were reading from in-memory array, does nothing.
     * <p>
     * @implNote Unfortunately, there is no simple way to close memory-mapped ByteBuffer in
     * Java and unmap underlying file. As {@link MappedByteBuffer} documentation suggests,
     * "mapped byte buffer and the file mapping that it represents remain valid until the
     * buffer itself is garbage-collected". Thus, the best we can do is to delete all
     * references to it, which breaks all subsequent <code>read..</code> methods with
     * {@link NullPointerException}. Afterwards, a call to {@link System#gc()} will
     * typically release the mmap, if garbage collection will be triggered.
     * </p>
     * <p>
     * There is a <a href="https://bugs.java.com/bugdatabase/view_bug.do?bug_id=4724038">
     * JDK-4724038 request for adding unmap method</a> filed at Java bugtracker since 2002,
     * but as of 2018, it is still unresolved.
     * </p>
     * <p>
     * A couple of unsafe approaches (such as using JNI, or using reflection to invoke JVM
     * internal APIs) have been suggested and used with some success, but these are either
     * unportable or dangerous (may crash JVM), so we're not using them in this general
     * purpose code.
     * </p>
     * <p>
     * For more examples and suggestions, see:
     * https://stackoverflow.com/questions/2972986/how-to-unmap-a-file-from-memory-mapped-using-filechannel-in-java
     * </p>
     * @throws IOException if FileChannel can't be closed
     */
    @Override
    public void close() throws IOException {
        if (fc != null) {
            fc.close();
            fc = null;
        }
        bb = null;
    }

    //region Stream positioning

    @Override
    public boolean isEof() {
        return !(bb.hasRemaining() || bitsLeft > 0);
    }

    @Override
    public void seek(int newPos) {
        bb.position(newPos);
    }

    @Override
    public void seek(long newPos) {
        if (newPos > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("Java ByteBuffer can't be seeked past Integer.MAX_VALUE");
        }
        bb.position((int) newPos);
    }

    @Override
    public int pos() {
        return bb.position();
    }

    @Override
    public long size() {
        return bb.limit();
    }

    //endregion

    //region Integer numbers

    //region Signed

    /**
     * Reads one signed 1-byte integer, returning it properly as Java's "byte" type.
     * @return 1-byte integer read from a stream
     */
    @Override
    public byte readS1() {
        return bb.get();
    }

    //region Big-endian

    @Override
    public short readS2be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getShort();
    }

    @Override
    public int readS4be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getInt();
    }

    @Override
    public long readS8be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getLong();
    }

    //endregion

    //region Little-endian

    @Override
    public short readS2le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getShort();
    }

    @Override
    public int readS4le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getInt();
    }

    @Override
    public long readS8le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getLong();
    }

    //endregion

    //endregion

    //region Unsigned

    @Override
    public int readU1() {
        return bb.get() & 0xff;
    }

    //region Big-endian

    @Override
    public int readU2be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getShort() & 0xffff;
    }

    @Override
    public long readU4be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getInt() & 0xffffffffL;
    }

    //endregion

    //region Little-endian

    @Override
    public int readU2le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getShort() & 0xffff;
    }

    @Override
    public long readU4le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getInt() & 0xffffffffL;
    }

    //endregion

    //endregion

    //endregion

    //region Floating point numbers

    //region Big-endian

    @Override
    public float readF4be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getFloat();
    }

    @Override
    public double readF8be() {
        bb.order(ByteOrder.BIG_ENDIAN);
        return bb.getDouble();
    }

    //endregion

    //region Little-endian

    @Override
    public float readF4le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getFloat();
    }

    @Override
    public double readF8le() {
        bb.order(ByteOrder.LITTLE_ENDIAN);
        return bb.getDouble();
    }

    //endregion

    //endregion

    //region Byte arrays

    /**
     * Reads designated number of bytes from the stream.
     * @param n number of bytes to read
     * @return read bytes as byte array
     */
    @Override
    public byte[] readBytes(long n) {
        byte[] buf = new byte[toByteArrayLength(n)];
        bb.get(buf);
        return buf;
    }

    /**
     * Reads all the remaining bytes in a stream as byte array.
     * @return all remaining bytes in a stream as byte array
     */
    @Override
    public byte[] readBytesFull() {
        byte[] buf = new byte[bb.remaining()];
        bb.get(buf);
        return buf;
    }

    @Override
    public byte[] readBytesTerm(int term, boolean includeTerm, boolean consumeTerm, boolean eosError) {
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        while (true) {
            if (!bb.hasRemaining()) {
                if (eosError) {
                    throw new RuntimeException("End of stream reached, but no terminator " + term + " found");
                } else {
                    return buf.toByteArray();
                }
            }
            int c = bb.get();
            if (c == term) {
                if (includeTerm)
                    buf.write(c);
                if (!consumeTerm)
                    bb.position(bb.position() - 1);
                return buf.toByteArray();
            }
            buf.write(c);
        }
    }

    //endregion
}
