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
  # python,
}:

let
  old_setuptools = setuptools.overrideAttrs (old: {
    version = "70.3.0";
    # src = fetchPypi {
    #   pname = "setuptools";
    #   version = "70.3.0";
    #   hash = "sha256-8XG6sd+8hrEymX8moRn2BWpXlQ0FhYeEGgCC6IMPncU=";
    # };
  });
    in
buildPythonPackage rec {
  pname = "endplay";
  version = "0.5.11";
  # pyproject = true;
  doCheck = false;
  # dontUseCmakeConfigure = true;
  # format = "wheel";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-2aCQD1Kz7olpbUODZNBvZxtBg8YIK3VjNXisuY9za+Y=";
    # dist = python;
    # python = "py3";
  };

  nativeBuildInputs = [
    cmake
    poetry-core
    old_setuptools
  ];

  buildInputs = [
    cmake
    poetry-core
    old_setuptools
  ];

  propagatedBuildInputs = [
    pyparsing
    tqdm
    numpy
    matplotlib
    more-itertools
  ];
  build-system = [
    setuptools
  ];


 #  nativeCheckInputs = [ pytestCheckHook pytest ];
 # checkPhase = ''
 #    runHook preCheck
 #    pytest
 #    python3 -m pytest

 #    runHook postCheck
 #  '';
  meta = {
    homepage = "https://github.com/dominicprice/endplay";
    description = "A Python library providing a variety of different tools for generating, analysing, solving and scoring bridge deals.";
    license = lib.licenses.mit;
    changelog = "https://github.com/dominicprice/endplay/releases/tag/v${version}";
  };
}
