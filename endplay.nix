{
  lib,
  buildPythonPackage,
  fetchPypi,

  # build dependencies
  setuptools,
  cmake,

  # dependencies
  pyparsing,
  tqdm,
  numpy,
  matplotlib,
  more-itertools,

  # tests
  pytestCheckHook,
}:

buildPythonPackage rec {
  pname = "endplay";
  version = "0.5.11";
  pyproject = true;
  doCheck = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-2aCQD1Kz7olpbUODZNBvZxtBg8YIK3VjNXisuY9za+Y=";
  };

  build-system = [ setuptools ];

  dependencies = [
    pyparsing
    tqdm
    numpy
    matplotlib
    more-itertools
  ];

  buildInpts = [ cmake ];

  nativeCheckInputs = [ pytestCheckHook ];

  meta = {
    homepage = "https://github.com/dominicprice/endplay";
    description = "A Python library providing a variety of different tools for generating, analysing, solving and scoring bridge deals.";
    # description = "Data description language";
    license = lib.licenses.mit;
    # };
    # meta = {
    changelog = "https://github.com/blaze/datashape/releases/tag/${version}";
    # homepage = "https://github.com/ContinuumIO/datashape";
  };
}
