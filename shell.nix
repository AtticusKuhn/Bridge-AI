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
        sha256 = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="; # Will be updated
      };
      doCheck = false;
      propagatedBuildInputs = [];
    })
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in
mkShell {
  buildInputs = [
    my-python
    pkgs.black
    pkgs.ruff
  ];
}
