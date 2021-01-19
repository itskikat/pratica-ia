
import pytest
import sof2018h

def test_exercicio15():
    assert round(sof2018h.bn.individualProb('pa', True),5) == 0.0163
