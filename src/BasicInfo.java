// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import io.kaitai.struct.ByteBufferKaitaiStream;
import io.kaitai.struct.KaitaiStruct;
import io.kaitai.struct.KaitaiStream;
import java.io.IOException;
import java.util.Map;
import java.util.HashMap;

public class BasicInfo extends KaitaiStruct {
    public static BasicInfo fromFile(String fileName) throws IOException {
        return new BasicInfo(new ByteBufferKaitaiStream(fileName));
    }

    public enum Status {
        OK(0),
        FAIL(128);

        private final long id;
        Status(long id) { this.id = id; }
        public long id() { return id; }
        private static final Map<Long, Status> byId = new HashMap<Long, Status>(2);
        static {
            for (Status e : Status.values())
                byId.put(e.id(), e);
        }
        public static Status byId(long id) { return byId.get(id); }
    }

    public BasicInfo(KaitaiStream _io) {
        this(_io, null, null);
    }

    public BasicInfo(KaitaiStream _io, KaitaiStruct _parent) {
        this(_io, _parent, null);
    }

    public BasicInfo(KaitaiStream _io, KaitaiStruct _parent, BasicInfo _root) {
        super(_io);
        this._parent = _parent;
        this._root = _root == null ? this : _root;
        _read();
    }
    private void _read() {
        this.magicStart = this._io.ensureFixedContents(new byte[] { -35 });
        this.magicCmd = this._io.ensureFixedContents(new byte[] { 3 });
        this.magicStatus = this._io.ensureFixedContents(new byte[] { 0 });
        this.dataLen = this._io.readU1();
    }
    private byte[] magicStart;
    private byte[] magicCmd;
    private byte[] magicStatus;
    private int dataLen;
    private BasicInfo _root;
    private KaitaiStruct _parent;
    public byte[] magicStart() { return magicStart; }
    public byte[] magicCmd() { return magicCmd; }
    public byte[] magicStatus() { return magicStatus; }
    public int dataLen() { return dataLen; }
    public BasicInfo _root() { return _root; }
    public KaitaiStruct _parent() { return _parent; }
}
