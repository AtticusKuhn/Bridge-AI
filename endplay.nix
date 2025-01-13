{
  lib,
  buildPythonPackage,
  fetchPypi,

  # build dependencies
  setuptools,
  cmake,
  poetry-core,
  # dependencies
  pyparsing,
  tqdm,
  numpy,
  matplotlib,
  more-itertools,

  # tests
  pytestCheckHook,
  pytest,
}:

buildPythonPackage rec {
  pname = "endplay";
  version = "0.5.11";
  pyproject = true;
  doCheck = true;
  dontUseCmakeConfigure = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-2aCQD1Kz7olpbUODZNBvZxtBg8YIK3VjNXisuY9za+Y=";
  };

  nativeBuildInputs = [ 
    cmake
    poetry-core
  ];

  buildInputs = [
    setuptools
  ];

  propagatedBuildInputs = [
    pyparsing
    tqdm
    numpy
    matplotlib
    more-itertools
  ];

  nativeCheckInputs = [ pytestCheckHook pytest ];
 checkPhase = ''
    runHook preCheck

    pytest
    python3 -m pytest


    runHook postCheck
  '';
  meta = {
    homepage = "https://github.com/dominicprice/endplay";
    description = "A Python library providing a variety of different tools for generating, analysing, solving and scoring bridge deals.";
    license = lib.licenses.mit;
    changelog = "https://github.com/dominicprice/endplay/releases/tag/v${version}";
  };
}
