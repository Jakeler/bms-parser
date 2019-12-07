import io.kaitai.struct.*;

public class Main {

	public static void main(String[] args) {
		byte[] input = int2byte(new int[]{0xdd, 0x03, 0x00, 0xff});
		BasicInfo info = new BasicInfo(new ByteBufferKaitaiStream(input));
		System.out.println(info.toString());
	}
	
	static byte[] int2byte(int[] in) {
		var out = new byte[in.length];
		for (int i = 0; i < in.length; i++) {
			out[i] = (byte) in[i];
		}
		return out;
	}

}
