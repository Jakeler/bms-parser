// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import io.kaitai.struct.ByteBufferKaitaiStream;
import io.kaitai.struct.KaitaiStruct;
import io.kaitai.struct.KaitaiStream;
import java.io.IOException;
import java.nio.charset.Charset;

public class AnimalRecord extends KaitaiStruct {
    public static AnimalRecord fromFile(String fileName) throws IOException {
        return new AnimalRecord(new ByteBufferKaitaiStream(fileName));
    }

    public AnimalRecord(KaitaiStream _io) {
        this(_io, null, null);
    }

    public AnimalRecord(KaitaiStream _io, KaitaiStruct _parent) {
        this(_io, _parent, null);
    }

    public AnimalRecord(KaitaiStream _io, KaitaiStruct _parent, AnimalRecord _root) {
        super(_io);
        this._parent = _parent;
        this._root = _root == null ? this : _root;
        _read();
    }
    private void _read() {
        this.uuid = this._io.readBytes(16);
        this.name = new String(this._io.readBytes(24), Charset.forName("UTF-8"));
        this.birthYear = this._io.readU2be();
        this.weight = this._io.readF8be();
        this.rating = this._io.readS4be();
    }
    private byte[] uuid;
    private String name;
    private int birthYear;
    private double weight;
    private int rating;
    private AnimalRecord _root;
    private KaitaiStruct _parent;
    public byte[] uuid() { return uuid; }
    public String name() { return name; }
    public int birthYear() { return birthYear; }
    public double weight() { return weight; }
    public int rating() { return rating; }
    public AnimalRecord _root() { return _root; }
    public KaitaiStruct _parent() { return _parent; }
}
