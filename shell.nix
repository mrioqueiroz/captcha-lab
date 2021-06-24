{ pkgs ? import (fetchTarball
  "https://github.com/NixOS/nixpkgs/archive/5272327b81ed355bbed5659b8d303cf2979b6953.tar.gz")
  { } }:

pkgs.mkShell {
  name = "captcha-lab";
  buildInputs = with pkgs; [
    python37
    python37Packages.jupyterlab
    python37Packages.pillow
    python37Packages.pip
    python37Packages.pytesseract
    tesseract
  ];
}
