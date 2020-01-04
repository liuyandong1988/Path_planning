package org.vrprep.translator.test;

import java.util.List;

import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.vrprep.translator.impl.ValueFetcher;

@RunWith(Parameterized.class)
public abstract class ValueFetcherTest {

	protected List<String> input;
	protected ValueFetcher fetcher;

	public ValueFetcherTest(List<String> input){
		this.input = input;
	}

}
