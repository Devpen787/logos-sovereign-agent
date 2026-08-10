#!/usr/bin/env node

import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const qtMcpRoot = process.env.LOGOS_QT_MCP || resolve("result-mcp");
const evidenceDir = process.env.BASECAMP_EVIDENCE_DIR || "basecamp-evidence";
const { test, run } = await import(
  resolve(qtMcpRoot, "test-framework/framework.mjs")
);

async function openModuleInspector(app) {
  await app.click("Settings");
  await app.waitFor(
    async () => {
      await app.expectTexts(["Dashboard", "Apps Inspector", "Module Inspector"]);
    },
    {
      timeout: 30000,
      interval: 500,
      description: "Basecamp Settings navigation",
    },
  );
  await app.click("Module Inspector", { type: "LogosItemDelegate" });
  await app.waitFor(
    async () => {
      await app.expectTexts([
        "Core modules known to the runtime, with live resource usage.",
        "Sovereign Agent",
        "sovereign_agent",
      ]);
    },
    {
      timeout: 30000,
      interval: 500,
      description: "sovereign_agent discovery in Module Inspector",
    },
  );
}

async function moduleInspectorId(app) {
  const result = await app.findByProperty("objectName", "moduleInspectorView");
  const match = result.matches?.[0];
  if (!match) {
    throw new Error("Basecamp moduleInspectorView was not found");
  }
  return match.id;
}

async function evaluateOnInspector(app, expression) {
  const objectId = await moduleInspectorId(app);
  const result = await app.inspector.send("evaluate", { objectId, expression });
  if (result.error) {
    throw new Error(`Basecamp evaluate failed: ${result.error}`);
  }
  return result.result;
}

async function callModule(app, method) {
  const raw = await evaluateOnInspector(
    app,
    `backend.callCoreModuleMethod("sovereign_agent", ${JSON.stringify(method)}, "[]")`,
  );
  return JSON.parse(raw);
}

async function waitForModuleState(app, expectedState) {
  await evaluateOnInspector(
    app,
    'showingInterface = false; searchText = "sovereign_agent"; backend.refreshCoreModules(); "refresh-requested"',
  );
  await app.waitFor(
    async () => {
      await app.expectTexts([
        "Sovereign Agent",
        "sovereign_agent",
        expectedState,
      ]);
    },
    {
      timeout: 30000,
      interval: 500,
      description: `sovereign_agent state ${expectedState}`,
    },
  );
  return {
    state: expectedState,
    source: "Basecamp filtered core module inspector",
  };
}

async function saveScreenshot(app, name) {
  const result = await app.screenshot();
  if (result.error || !result.image) {
    throw new Error(`Basecamp screenshot failed: ${result.error || "no image"}`);
  }
  mkdirSync(evidenceDir, { recursive: true });
  writeFileSync(resolve(evidenceDir, name), Buffer.from(result.image, "base64"));
}

test("Basecamp loads and drives the sovereign agent public contract", async (app) => {
  await openModuleInspector(app);

  await evaluateOnInspector(app, 'backend.loadCoreModule("sovereign_agent")');
  let version;
  await app.waitFor(
    async () => {
      version = await callModule(app, "version");
      if (version.result !== "0.1.0") {
        throw new Error(`unexpected version result: ${JSON.stringify(version)}`);
      }
    },
    {
      timeout: 30000,
      interval: 500,
      description: "sovereign_agent loaded and callable in Basecamp",
    },
  );

  const methods = JSON.parse(
    await evaluateOnInspector(
      app,
      'backend.getCoreModuleMethods("sovereign_agent")',
    ),
  );
  const events = JSON.parse(
    await evaluateOnInspector(
      app,
      'backend.getCoreModuleEvents("sovereign_agent")',
    ),
  );
  const methodNames = new Set(methods.map((item) => item.name));
  const eventNames = new Set(events.map((item) => item.name));
  if (
    !methodNames.has("version") ||
    !methodNames.has("status") ||
    !methodNames.has("chatDependencyHealthy")
  ) {
    throw new Error(`public methods missing: ${JSON.stringify(methods)}`);
  }
  if (!eventNames.has("statusChanged")) {
    throw new Error(`public event missing: ${JSON.stringify(events)}`);
  }

  const status = await callModule(app, "status");
  const chatDependencyHealthy = await callModule(
    app,
    "chatDependencyHealthy",
  );
  if (chatDependencyHealthy.result !== true) {
    throw new Error(
      `chat dependency did not answer through typed composition: ${JSON.stringify(chatDependencyHealthy)}`,
    );
  }
  const decodedStatus = JSON.parse(status.result);
  const expectedStatus = {
    module: "sovereign_agent",
    state: "native_spike",
    version: "0.1.0",
  };
  if (JSON.stringify(decodedStatus) !== JSON.stringify(expectedStatus)) {
    throw new Error(`unexpected status result: ${JSON.stringify(status)}`);
  }

  await evaluateOnInspector(
    app,
    'openInterface("sovereign_agent"); "interface-opened"',
  );
  await app.waitFor(
    async () => {
      await app.expectTexts([
        "Interface: sovereign_agent",
        "Methods",
        "version",
        "status",
        "chatDependencyHealthy",
        "Events",
        "statusChanged",
      ]);
    },
    {
      timeout: 30000,
      interval: 500,
      description: "Basecamp public interface rendering",
    },
  );
  await saveScreenshot(app, "basecamp-sovereign-agent-interface.png");

  await evaluateOnInspector(app, 'backend.unloadCoreModule("sovereign_agent")');
  const unloaded = await waitForModuleState(app, "Not loaded");

  await evaluateOnInspector(app, 'backend.loadCoreModule("sovereign_agent")');
  const reloaded = await waitForModuleState(app, "Loaded");
  let afterReload;
  await app.waitFor(
    async () => {
      afterReload = await callModule(app, "status");
      if (JSON.parse(afterReload.result).state !== "native_spike") {
        throw new Error(`bad post-reload status: ${JSON.stringify(afterReload)}`);
      }
    },
    {
      timeout: 30000,
      interval: 500,
      description: "sovereign_agent reload and call",
    },
  );

  mkdirSync(evidenceDir, { recursive: true });
  writeFileSync(
    resolve(evidenceDir, "basecamp-contract.json"),
    JSON.stringify(
      {
        module: "sovereign_agent",
        version,
        status,
        chatDependencyHealthy,
        methods,
        events,
        unloaded,
        reloaded,
        afterReload,
      },
      null,
      2,
    ) + "\n",
  );
});

run();
