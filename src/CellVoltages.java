// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import io.kaitai.struct.ByteBufferKaitaiStream;
import io.kaitai.struct.KaitaiStruct;
import io.kaitai.struct.KaitaiStream;
import java.io.IOException;
import java.util.ArrayList;

public class CellVoltages extends KaitaiStruct {
    public static CellVoltages fromFile(String fileName) throws IOException {
        return new CellVoltages(new ByteBufferKaitaiStream(fileName));
    }

    public CellVoltages(KaitaiStream _io) {
        this(_io, null, null);
    }

    public CellVoltages(KaitaiStream _io, KaitaiStruct _parent) {
        this(_io, _parent, null);
    }

    public CellVoltages(KaitaiStream _io, KaitaiStruct _parent, CellVoltages _root) {
        super(_io);
        this._parent = _parent;
        this._root = _root == null ? this : _root;
        _read();
    }
    private void _read() {
        this.magicStart = this._io.ensureFixedContents(new byte[] { -35 });
        this.magicCmd = this._io.ensureFixedContents(new byte[] { 4 });
        this.magicStatus = this._io.ensureFixedContents(new byte[] { 0 });
        this.dataLen = this._io.readU1();
        cells = new ArrayList<Integer>((int) (count()));
        for (int i = 0; i < count(); i++) {
            this.cells.add(this._io.readU2be());
        }
        this.checksum = this._io.readBytes(2);
        this.magicEnd = this._io.ensureFixedContents(new byte[] { 119 });
    }
    private Integer count;
    public Integer count() {
        if (this.count != null)
            return this.count;
        int _tmp = (int) ((dataLen() / 2));
        this.count = _tmp;
        return this.count;
    }
    private byte[] magicStart;
    private byte[] magicCmd;
    private byte[] magicStatus;
    private int dataLen;
    private ArrayList<Integer> cells;
    private byte[] checksum;
    private byte[] magicEnd;
    private CellVoltages _root;
    private KaitaiStruct _parent;
    public byte[] magicStart() { return magicStart; }
    public byte[] magicCmd() { return magicCmd; }
    public byte[] magicStatus() { return magicStatus; }
    public int dataLen() { return dataLen; }

    /**
     * Cell voltages in mV
     */
    public ArrayList<Integer> cells() { return cells; }
    public byte[] checksum() { return checksum; }
    public byte[] magicEnd() { return magicEnd; }
    public CellVoltages _root() { return _root; }
    public KaitaiStruct _parent() { return _parent; }
}
