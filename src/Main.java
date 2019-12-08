import io.kaitai.struct.*;

import java.lang.reflect.Array;
import java.util.Arrays;

public class Main {

	public static void main(String[] args) {
		byte[] input = int2byte(new int[]{
				0xdd, 0x03, 0x00, 0x1b, 0x11, 0x38, 0x00, 0x62,
				0x00, 0xa4, 0x04, 0xb0, 0x00, 0x00, 0x27, 0x6e,
				0x02, 0x82, 0x00, 0x00, 0x00, 0x00, 0x21, 0x0e,
				0x03, 0x0b, 0x02, 0x0b, 0x22, 0x0b, 0x10, 0xfc,
				0x42, 0x77});

		byte[] input2 = int2byte(new int[]{
			0xdd, 0x04, 0x00, 0x16, 0x0f, 0xa7, 0x0f, 0xa5,
			0x0f, 0xa1, 0x0f, 0x98, 0x0f, 0x9e, 0x0f, 0xa0,
			0x0f, 0xb1, 0x0f, 0xbb, 0x0f, 0xb1, 0x0f, 0xa6,
			0x0f, 0xa7, 0xf8, 0x18, 0x77});

		var info = new BasicInfo(new ByteBufferKaitaiStream(input));
		var cells = new CellVoltages(new ByteBufferKaitaiStream(input2));
		printInfo(info, cells);
	}

	static void printInfo(BasicInfo info, CellVoltages cells) {
		System.out.println("Pack voltage: " + info.totalV() + " V");
		System.out.println("Current: " + info.currentA()  + " A");
		System.out.printf("Remaining capacity: %f Ah (%d %%)\n", info.remainCapAh(), info.data().remainCapPercent());
		System.out.println("Balancing " + info.data().balanceStatus().flag());
		System.out.println("Protection " + info.data().protStatus().toString());
		System.out.println("Charge:"+ info.data().fetStatus().charge() + " Discharge:" + info.data().fetStatus().charge());
		System.out.println("Cycle count = " + info.data().cycles());
		System.out.printf("Temp1: %f C, Temp2: %f C\n", tempToCelsius(info.data().tempValue().get(0)), tempToCelsius(info.data().tempValue().get(1)));

		System.out.println("Count " + cells.count());
		System.out.println("Cells " + cells.cells());
	}

	static double tempToCelsius(int raw) {
		return (raw - 2731) * 0.1;
	}
	
	static byte[] int2byte(int[] in) {
		var out = new byte[in.length];
		for (int i = 0; i < in.length; i++) {
			out[i] = (byte) in[i];
		}
		return out;
	}

}
