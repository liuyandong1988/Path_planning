package org.vrprep.translator.test.tsplib95;

import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import org.junit.Test;
import org.junit.runners.Parameterized;
import org.vrprep.translator.impl.tsplib95.TSPLIB95ValueFetcher;
import org.vrprep.translator.test.ValueFetcherTest;

public class TSPLIB95ValueFetcherTest extends ValueFetcherTest {

	private int numberOfKeywords;

	public TSPLIB95ValueFetcherTest(List<String> input, int numberOfKeywords) {
		super(input);
		this.fetcher = new TSPLIB95ValueFetcher();
		fetcher.initialize(input);
		this.numberOfKeywords = numberOfKeywords;
	}

	@Parameterized.Parameters
	public static Collection<?> data() {

		List<String> input1 = Arrays.asList(new String[]{
				"NAME : D022-04g",
				"COMMENT :",
				"TYPE: ",
				"DIMENSION : 22",
				"CAPACITY : 6000",
				"EDGE_WEIGHT_TYPE : EUC_2D",
				"EDGE_WEIGHT_FORMAT: FUNCTION",
				"NODE_COORD_TYPE : TWOD_COORDS",
				"DISPLAY_DATA_TYPE : COORD_DISPLAY",
				"DISTANCE : 210.00",
				"SERVICE_TIME : 0",
				"VEHICLES : 4",
				"NODE_COORD_SECTION",
				"1 23 -33",
				"2 3 -3",
				"3 12 -12"
		});

		return Arrays.asList(new Object[][] {
				{input1, 13}
		});
	}

	@Test
	public void testNumberOfKeywords() {
		assertEquals(fetcher.getKeywords().length, numberOfKeywords);
	}

}
