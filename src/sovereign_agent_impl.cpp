#include "sovereign_agent_impl.h"

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
