{
  description = "Logos Sovereign Agent native module";

  inputs = {
    logos-module-builder.url = "github:logos-co/logos-module-builder/2b59cb8e855894f7e7a064b15bfae409f288080b";
  };

  outputs = inputs@{ logos-module-builder, ... }:
    logos-module-builder.lib.mkLogosModule {
      src = ./.;
      configFile = ./metadata.json;
      flakeInputs = inputs;
    };
}
