// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import io.kaitai.struct.ByteBufferKaitaiStream;
import io.kaitai.struct.KaitaiStruct;
import io.kaitai.struct.KaitaiStream;
import java.io.IOException;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

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

    public enum FetBit {
        FALSE(0),
        TRUE(1);

        private final long id;
        FetBit(long id) { this.id = id; }
        public long id() { return id; }
        private static final Map<Long, FetBit> byId = new HashMap<Long, FetBit>(2);
        static {
            for (FetBit e : FetBit.values())
                byId.put(e.id(), e);
        }
        public static FetBit byId(long id) { return byId.get(id); }
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
        this._raw_data = this._io.readBytes(dataLen());
        KaitaiStream _io__raw_data = new ByteBufferKaitaiStream(_raw_data);
        this.data = new DataBlock(_io__raw_data, this, _root);
        this.checksum = this._io.readBytes(2);
        this.magicEnd = this._io.ensureFixedContents(new byte[] { 119 });
    }
    public static class BalanceList extends KaitaiStruct {
        public static BalanceList fromFile(String fileName) throws IOException {
            return new BalanceList(new ByteBufferKaitaiStream(fileName));
        }

        public BalanceList(KaitaiStream _io) {
            this(_io, null, null);
        }

        public BalanceList(KaitaiStream _io, BasicInfo.DataBlock _parent) {
            this(_io, _parent, null);
        }

        public BalanceList(KaitaiStream _io, BasicInfo.DataBlock _parent, BasicInfo _root) {
            super(_io);
            this._parent = _parent;
            this._root = _root;
            _read();
        }
        private void _read() {
            flag = new ArrayList<Boolean>((int) ((4 * 8)));
            for (int i = 0; i < (4 * 8); i++) {
                this.flag.add(this._io.readBitsInt(1) != 0);
            }
        }
        private ArrayList<Boolean> flag;
        private BasicInfo _root;
        private BasicInfo.DataBlock _parent;
        public ArrayList<Boolean> flag() { return flag; }
        public BasicInfo _root() { return _root; }
        public BasicInfo.DataBlock _parent() { return _parent; }
    }
    public static class ProtList extends KaitaiStruct {
        public static ProtList fromFile(String fileName) throws IOException {
            return new ProtList(new ByteBufferKaitaiStream(fileName));
        }

        public ProtList(KaitaiStream _io) {
            this(_io, null, null);
        }

        public ProtList(KaitaiStream _io, BasicInfo.DataBlock _parent) {
            this(_io, _parent, null);
        }

        public ProtList(KaitaiStream _io, BasicInfo.DataBlock _parent, BasicInfo _root) {
            super(_io);
            this._parent = _parent;
            this._root = _root;
            _read();
        }
        private void _read() {
            this.ovpCell = this._io.readBitsInt(1) != 0;
            this.uvpCell = this._io.readBitsInt(1) != 0;
            this.ovpPack = this._io.readBitsInt(1) != 0;
            this.uvpPack = this._io.readBitsInt(1) != 0;
            this.otpCharge = this._io.readBitsInt(1) != 0;
            this.utpCharge = this._io.readBitsInt(1) != 0;
            this.otpDischarge = this._io.readBitsInt(1) != 0;
            this.utpDischarge = this._io.readBitsInt(1) != 0;
            this.ocpCharge = this._io.readBitsInt(1) != 0;
            this.ocpDischarge = this._io.readBitsInt(1) != 0;
            this.ocpShort = this._io.readBitsInt(1) != 0;
            this.icError = this._io.readBitsInt(1) != 0;
            this.fetLock = this._io.readBitsInt(1) != 0;
        }
        private boolean ovpCell;
        private boolean uvpCell;
        private boolean ovpPack;
        private boolean uvpPack;
        private boolean otpCharge;
        private boolean utpCharge;
        private boolean otpDischarge;
        private boolean utpDischarge;
        private boolean ocpCharge;
        private boolean ocpDischarge;
        private boolean ocpShort;
        private boolean icError;
        private boolean fetLock;
        private BasicInfo _root;
        private BasicInfo.DataBlock _parent;
        public boolean ovpCell() { return ovpCell; }
        public boolean uvpCell() { return uvpCell; }
        public boolean ovpPack() { return ovpPack; }
        public boolean uvpPack() { return uvpPack; }
        public boolean otpCharge() { return otpCharge; }
        public boolean utpCharge() { return utpCharge; }
        public boolean otpDischarge() { return otpDischarge; }
        public boolean utpDischarge() { return utpDischarge; }
        public boolean ocpCharge() { return ocpCharge; }
        public boolean ocpDischarge() { return ocpDischarge; }
        public boolean ocpShort() { return ocpShort; }
        public boolean icError() { return icError; }
        public boolean fetLock() { return fetLock; }
        public BasicInfo _root() { return _root; }
        public BasicInfo.DataBlock _parent() { return _parent; }

        @Override
        public String toString() {
            return "ProtList{" +
                    "ovpCell=" + ovpCell +
                    ", uvpCell=" + uvpCell +
                    ", ovpPack=" + ovpPack +
                    ", uvpPack=" + uvpPack +
                    ", otpCharge=" + otpCharge +
                    ", utpCharge=" + utpCharge +
                    ", otpDischarge=" + otpDischarge +
                    ", utpDischarge=" + utpDischarge +
                    ", ocpCharge=" + ocpCharge +
                    ", ocpDischarge=" + ocpDischarge +
                    ", ocpShort=" + ocpShort +
                    ", icError=" + icError +
                    ", fetLock=" + fetLock +
                    '}';
        }
    }
    public static class FetBits extends KaitaiStruct {
        public static FetBits fromFile(String fileName) throws IOException {
            return new FetBits(new ByteBufferKaitaiStream(fileName));
        }

        public FetBits(KaitaiStream _io) {
            this(_io, null, null);
        }

        public FetBits(KaitaiStream _io, BasicInfo.DataBlock _parent) {
            this(_io, _parent, null);
        }

        public FetBits(KaitaiStream _io, BasicInfo.DataBlock _parent, BasicInfo _root) {
            super(_io);
            this._parent = _parent;
            this._root = _root;
            _read();
        }
        private void _read() {
            this.charge = BasicInfo.FetBit.byId(this._io.readBitsInt(1));
            this.discharge = BasicInfo.FetBit.byId(this._io.readBitsInt(1));
        }
        private FetBit charge;
        private FetBit discharge;
        private BasicInfo _root;
        private BasicInfo.DataBlock _parent;
        public FetBit charge() { return charge; }
        public FetBit discharge() { return discharge; }
        public BasicInfo _root() { return _root; }
        public BasicInfo.DataBlock _parent() { return _parent; }
    }
    public static class DataBlock extends KaitaiStruct {
        public static DataBlock fromFile(String fileName) throws IOException {
            return new DataBlock(new ByteBufferKaitaiStream(fileName));
        }

        public DataBlock(KaitaiStream _io) {
            this(_io, null, null);
        }

        public DataBlock(KaitaiStream _io, BasicInfo _parent) {
            this(_io, _parent, null);
        }

        public DataBlock(KaitaiStream _io, BasicInfo _parent, BasicInfo _root) {
            super(_io);
            this._parent = _parent;
            this._root = _root;
            _read();
        }
        private void _read() {
            this.total = this._io.readU2be();
            this.current = this._io.readU2be();
            this.remainCap = this._io.readU2be();
            this.typCap = this._io.readU2be();
            this.cycles = this._io.readU2be();
            this.prodDate = this._io.readU2be();
            this.balanceStatus = new BalanceList(this._io, this, _root);
            this._raw_protStatus = this._io.readBytes(2);
            KaitaiStream _io__raw_protStatus = new ByteBufferKaitaiStream(_raw_protStatus);
            this.protStatus = new ProtList(_io__raw_protStatus, this, _root);
            this.softwareVersion = this._io.readU1();
            this.remainCapPercent = this._io.readU1();
            this._raw_fetStatus = this._io.readBytes(1);
            KaitaiStream _io__raw_fetStatus = new ByteBufferKaitaiStream(_raw_fetStatus);
            this.fetStatus = new FetBits(_io__raw_fetStatus, this, _root);
            this.cellCount = this._io.readU1();
            this.tempCount = this._io.readU1();
            tempValue = new ArrayList<Integer>((int) (tempCount()));
            for (int i = 0; i < tempCount(); i++) {
                this.tempValue.add(this._io.readU2be());
            }
        }
        private int total;
        private int current;
        private int remainCap;
        private int typCap;
        private int cycles;
        private int prodDate;
        private BalanceList balanceStatus;
        private ProtList protStatus;
        private int softwareVersion;
        private int remainCapPercent;
        private FetBits fetStatus;
        private int cellCount;
        private int tempCount;
        private ArrayList<Integer> tempValue;
        private BasicInfo _root;
        private BasicInfo _parent;
        private byte[] _raw_protStatus;
        private byte[] _raw_fetStatus;

        /**
         * Pack voltage (raw)
         */
        public int total() { return total; }

        /**
         * Actual current (raw)
         */
        public int current() { return current; }

        /**
         * Capacity (raw)
         */
        public int remainCap() { return remainCap; }

        /**
         * Capacity (raw)
         */
        public int typCap() { return typCap; }

        /**
         * Cycle times
         */
        public int cycles() { return cycles; }

        /**
         * Production date
         */
        public int prodDate() { return prodDate; }

        /**
         * List of balance bits
         */
        public BalanceList balanceStatus() { return balanceStatus; }

        /**
         * List of protection bits
         */
        public ProtList protStatus() { return protStatus; }
        public int softwareVersion() { return softwareVersion; }

        /**
         * Portion of remaining capacity
         */
        public int remainCapPercent() { return remainCapPercent; }
        public FetBits fetStatus() { return fetStatus; }
        public int cellCount() { return cellCount; }
        public int tempCount() { return tempCount; }
        public ArrayList<Integer> tempValue() { return tempValue; }
        public BasicInfo _root() { return _root; }
        public BasicInfo _parent() { return _parent; }
        public byte[] _raw_protStatus() { return _raw_protStatus; }
        public byte[] _raw_fetStatus() { return _raw_fetStatus; }
    }
    private Double totalV;

    /**
     * Pack voltage (V)
     */
    public Double totalV() {
        if (this.totalV != null)
            return this.totalV;
        double _tmp = (double) ((data().total() * 0.01));
        this.totalV = _tmp;
        return this.totalV;
    }
    private Double currentA;

    /**
     * Actual current (A)
     */
    public Double currentA() {
        if (this.currentA != null)
            return this.currentA;
        double _tmp = (double) ((data().current() * 0.01));
        this.currentA = _tmp;
        return this.currentA;
    }
    private Double remainCapAh;

    /**
     * Capacity (Ah)
     */
    public Double remainCapAh() {
        if (this.remainCapAh != null)
            return this.remainCapAh;
        double _tmp = (double) ((data().remainCap() * 0.01));
        this.remainCapAh = _tmp;
        return this.remainCapAh;
    }
    private Double typCapAh;

    /**
     * Capacity (Ah)
     */
    public Double typCapAh() {
        if (this.typCapAh != null)
            return this.typCapAh;
        double _tmp = (double) ((data().typCap() * 0.01));
        this.typCapAh = _tmp;
        return this.typCapAh;
    }
    private byte[] magicStart;
    private byte[] magicCmd;
    private byte[] magicStatus;
    private int dataLen;
    private DataBlock data;
    private byte[] checksum;
    private byte[] magicEnd;
    private BasicInfo _root;
    private KaitaiStruct _parent;
    private byte[] _raw_data;
    public byte[] magicStart() { return magicStart; }
    public byte[] magicCmd() { return magicCmd; }
    public byte[] magicStatus() { return magicStatus; }
    public int dataLen() { return dataLen; }
    public DataBlock data() { return data; }
    public byte[] checksum() { return checksum; }
    public byte[] magicEnd() { return magicEnd; }
    public BasicInfo _root() { return _root; }
    public KaitaiStruct _parent() { return _parent; }
    public byte[] _raw_data() { return _raw_data; }
}
