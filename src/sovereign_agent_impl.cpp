#include "sovereign_agent_impl.h"

// Generated from metadata.json's declared chat_module dependency. Keeping this
// include in the implementation leaves the public contract Qt-free.
#include "logos_sdk.h"

std::string SovereignAgentImpl::version()
{
    return "0.1.0";
}

std::string SovereignAgentImpl::status()
{
    const std::string result =
        R"({"module":"sovereign_agent","state":"native_spike","version":"0.1.0"})";
    statusChanged(result);
    return result;
}

bool SovereignAgentImpl::chatDependencyHealthy()
{
    return modules().chat_module.health();
}
