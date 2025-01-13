{ pkgs ? import <nixpkgs> {} }:
with pkgs;let
  my-python-packages = ps: with ps; [
    pytorch
    matplotlib
    numpy
    (buildPythonPackage rec {
      pname = "endplay";
      version = "0.5.11";
      src = fetchPypi {
        inherit pname version;
        sha256 = "sha256-2aCQD1Kz7olpbUODZNBvZxtBg8YIK3VjNXisuY9za+Y=";
      };
      doCheck = false;
      nativeBuildInputs = [
        pkgs.cmake
        (pkgs.python3Packages.setuptools.overridePythonAttrs (old: {
          version = "70.3.0";
          src = pkgs.fetchPypi {
            pname = "setuptools";
            version = "70.3.0";
            sha256 = "sha256-YlBwVxhzwJyf8h/a/kK3Oj2P2wXvwJqP1lB+sF3xkDY=";
          };
        }))
        pkgs.python3Packages.wheel
        pkgs.python3Packages.pip
        pkgs.python3Packages.scikit-build
        pkgs.python3Packages.poetry-core
      ];
      buildInputs = [];
      propagatedBuildInputs = [];
      dontUseCmakeConfigure = true;
      format = "pyproject";
    })
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in
mkShell {
  buildInputs = [
    my-python
    pkgs.black
    pkgs.ruff
    pkgs.cmake
  ];
}
