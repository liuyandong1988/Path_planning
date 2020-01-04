package org.vrprep.translator.test;

import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.Collection;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.vrprep.translator.util.TimestampComparator;

@RunWith(Parameterized.class)
public class TimestampComparatorTest {
	
	private TimestampComparator comparator;
	private String timestamp1;
	private String timestamp2;
	private int difference;
	
	public TimestampComparatorTest(String timestamp1, String timestamp2, int difference) {
		this.comparator = new TimestampComparator();
		this.timestamp1 = timestamp1;
		this.timestamp2 = timestamp2;
		this.difference = difference;
	}
	
	@Parameterized.Parameters
	public static Collection<?> data() {
		return Arrays.asList(new Object[][] {
				{"2:30", "3:45", -75},
				{"8:00", "9:50", -110},
				{"15:17", "12:52", 145},
				{"7:00", "6:59", 1},
				{"23:59", "0:00", 1439}
		});

	}

	@Test
	public void test() {
		assertEquals(comparator.compare(timestamp1, timestamp2), difference);
	}

}
