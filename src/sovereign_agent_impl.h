#pragma once

#include <string>

#include "logos_module_context.h"

class SovereignAgentImpl : public LogosModuleContext
{
public:
    /// Returns the public module-contract version.
    std::string version();

    /// Returns deterministic JSON describing this bounded native spike.
    std::string status();

logos_events:
    /// Emitted with the exact status value returned by status().
    void statusChanged(const std::string& status);
};
