# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    requests
    msal
    google-api-python-client
    google-auth-httplib2
    google-auth-oauthlib
    icalendar
    psycopg2
    (
      buildPythonPackage rec {
        pname = "O365";
        version = "2.0.31";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-BbNnpY5HzFNvWKm78loaEAg6m+PF0v1+/EXJrQFbh9A=";
        };
        doCheck = false;
        propagatedBuildInputs = [
          # Specify dependencies
          pkgs.python3Packages.oauthlib
          pkgs.python3Packages.requests_oauthlib
          pkgs.python3Packages.stringcase
          pkgs.python3Packages.tzlocal
          pkgs.python3Packages.dateutil
          pkgs.python3Packages.beautifulsoup4
        ];
      }
    )
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
