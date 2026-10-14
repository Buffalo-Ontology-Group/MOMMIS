# Portable interface

Download `mommis-explorer.html` using GitHub's **Download raw file** button, then open the downloaded file in a browser. GitHub's normal file page displays HTML source, not the running interface. The interface has a visible link to MOMMIS PR #2.

This is a generated snapshot for review. To refresh it after explorer changes:

```sh
npm run build:standalone
cp dist/mommis-explorer.html preview/mommis-explorer.html
```

The draft ontology is at `../ontology/mommis-milk-core.owl`; open that file separately in Protégé. The interface does not yet load or reason over the OWL file.
