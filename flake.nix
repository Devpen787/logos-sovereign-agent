{
  description = "Logos Sovereign Agent native module";

  inputs = {
    chat_module.url = "github:logos-co/logos-chat-module/dfe8ccf3eff3e95da0ba54043577270474a216ae";
    logos-module-builder.follows = "chat_module/logos-module-builder";
  };

  outputs = inputs@{ logos-module-builder, chat_module, ... }:
    logos-module-builder.lib.mkLogosModule {
      src = ./.;
      configFile = ./metadata.json;
      flakeInputs = inputs;
    };
}
