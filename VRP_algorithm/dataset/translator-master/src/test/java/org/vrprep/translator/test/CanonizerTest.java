package org.vrprep.translator.test;

import java.util.Map;

import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.vrprep.translator.impl.Canonizer;
import org.vrprep.translator.impl.Keyword;

@RunWith(Parameterized.class)
public abstract class CanonizerTest {

	protected Map<Keyword, String> map;
	protected Canonizer canonizer;

	public CanonizerTest(Map<Keyword, String> map) {
		this.map = map;
	}

}
