{
  pkgs ? import <nixpkgs> { },
}:
with pkgs;
let
  # endplay = python312.pkgs.buildPythonPackage rec {
  #   pname = "endplay";
  #   version = "0.5.11";
  #   pyproject = true;

  #   src = fetchPypi {
  #     inherit pname version;
  #     hash = "sha256-2aCQD1Kz7olpbUODZNBvZxtBg8YIK3VjNXisuY9za+Y=";
  #   };

  #   build-system = [ python312.pkgs.setuptools ];
  #   # has no tests
  #   # doCheck = false;

  #   meta = {
  #     homepage = "https://github.com/dominicprice/endplay";
  #     description = "A Python library providing a variety of different tools for generating, analysing, solving and scoring bridge deals.";
  #   };
  # };
  endplay = ps: ps.callPackage ./endplay.nix {};
  my-python-packages =
    ps: with ps; [
      pytorch
      matplotlib
      numpy
      pip
      more-itertools
      # (endplay ps)
      # ps.callPackage ./endplay.nix {}
    ];
  my-python = pkgs.python3.withPackages my-python-packages;
in
mkShell {
  buildInputs = with pkgs;[
    my-python
    black
    ruff
    nixfmt-rfc-style
    # uv
  ];
}
