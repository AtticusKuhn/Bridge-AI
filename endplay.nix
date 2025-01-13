{
  lib,
  buildPythonPackage,
  fetchPypi,

  # build dependencies
  setuptools_70_3_0 ? setuptools.overrideAttrs (old: {
    version = "70.3.0";
    src = fetchPypi {
      pname = "setuptools";
      version = "70.3.0";
      hash = "sha256-Hy7d5EFmGrR/QMWP0nSHXh0mXHGdmHPFYXvXA5O788=";
    };
  }),
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
    setuptools_70_3_0
  ];

  buildInputs = [
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
