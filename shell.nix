{ pkgs ? import <nixpkgs-unstable> {} }:
with pkgs;let
  my-python-packages = ps: with ps; [
    numpy
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
