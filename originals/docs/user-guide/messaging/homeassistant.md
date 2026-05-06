On this page
Hermes Agent integrates with [Home Assistant](<https://www.home-assistant.io/>) in two ways:
  1. **Gateway platform** — subscribes to real-time state changes via WebSocket and responds to events
  2. **Smart home tools** — four LLM-callable tools for querying and controlling devices via the REST API


## Setup[​](<#setup> "Direct link to Setup")
### 1\. Create a Long-Lived Access Token[​](<#1-create-a-long-lived-access-token> "Direct link to 1. Create a Long-Lived Access Token")
  1. Open your Home Assistant instance
  2. Go to your **Profile** (click your name in the sidebar)
  3. Scroll to **Long-Lived Access Tokens**
  4. Click **Create Token** , give it a name like "Hermes Agent"
  5. Copy the token


### 2\. Configure Environment Variables[​](<#2-configure-environment-variables> "Direct link to 2. Configure Environment Variables")
[code] 
    # Add to ~/.hermes/.env  
      
    # Required: your Long-Lived Access Token  
    HASS_TOKEN=your-long-lived-access-token  
      
    # Optional: HA URL (default: http://homeassistant.local:8123)  
    HASS_URL=http://192.168.1.100:8123  
    
[/code]
info
The `homeassistant` toolset is automatically enabled when `HASS_TOKEN` is set. Both the gateway platform and the device control tools activate from this single token.
### 3\. Start the Gateway[​](<#3-start-the-gateway> "Direct link to 3. Start the Gateway")
[code] 
    hermes gateway  
    
[/code]
Home Assistant will appear as a connected platform alongside any other messaging platforms (Telegram, Discord, etc.).
## Available Tools[​](<#available-tools> "Direct link to Available Tools")
Hermes Agent registers four tools for smart home control:
### `ha_list_entities`[​](<#ha_list_entities> "Direct link to ha_list_entities")
List Home Assistant entities, optionally filtered by domain or area.
**Parameters:**
  * `domain` _(optional)_ — Filter by entity domain: `light`, `switch`, `climate`, `sensor`, `binary_sensor`, `cover`, `fan`, `media_player`, etc.
  * `area` _(optional)_ — Filter by area/room name (matches against friendly names): `living room`, `kitchen`, `bedroom`, etc.


**Example:**
[code] 
    List all lights in the living room  
    
[/code]
Returns entity IDs, states, and friendly names.
### `ha_get_state`[​](<#ha_get_state> "Direct link to ha_get_state")
Get detailed state of a single entity, including all attributes (brightness, color, temperature setpoint, sensor readings, etc.).
**Parameters:**
  * `entity_id` _(required)_ — The entity to query, e.g., `light.living_room`, `climate.thermostat`, `sensor.temperature`


**Example:**
[code] 
    What's the current state of climate.thermostat?  
    
[/code]
Returns: state, all attributes, last changed/updated timestamps.
### `ha_list_services`[​](<#ha_list_services> "Direct link to ha_list_services")
List available services (actions) for device control. Shows what actions can be performed on each device type and what parameters they accept.
**Parameters:**
  * `domain` _(optional)_ — Filter by domain, e.g., `light`, `climate`, `switch`


**Example:**
[code] 
    What services are available for climate devices?  
    
[/code]
### `ha_call_service`[​](<#ha_call_service> "Direct link to ha_call_service")
Call a Home Assistant service to control a device.
**Parameters:**
  * `domain` _(required)_ — Service domain: `light`, `switch`, `climate`, `cover`, `media_player`, `fan`, `scene`, `script`
  * `service` _(required)_ — Service name: `turn_on`, `turn_off`, `toggle`, `set_temperature`, `set_hvac_mode`, `open_cover`, `close_cover`, `set_volume_level`
  * `entity_id` _(optional)_ — Target entity, e.g., `light.living_room`
  * `data` _(optional)_ — Additional parameters as a JSON object


**Examples:**
[code] 
    Turn on the living room lights  
    → ha_call_service(domain="light", service="turn_on", entity_id="light.living_room")  
    
[/code]
[code] 
    Set the thermostat to 22 degrees in heat mode  
    → ha_call_service(domain="climate", service="set_temperature",  
        entity_id="climate.thermostat", data={"temperature": 22, "hvac_mode": "heat"})  
    
[/code]
[code] 
    Set living room lights to blue at 50% brightness  
    → ha_call_service(domain="light", service="turn_on",  
        entity_id="light.living_room", data={"brightness": 128, "color_name": "blue"})  
    
[/code]
## Gateway Platform: Real-Time Events[​](<#gateway-platform-real-time-events> "Direct link to Gateway Platform: Real-Time Events")
The Home Assistant gateway adapter connects via WebSocket and subscribes to `state_changed` events. When a device state changes and matches your filters, it's forwarded to the agent as a message.
### Event Filtering[​](<#event-filtering> "Direct link to Event Filtering")
Required Configuration
By default, **no events are forwarded**. You must configure at least one of `watch_domains`, `watch_entities`, or `watch_all` to receive events. Without filters, a warning is logged at startup and all state changes are silently dropped.
Configure which events the agent sees in `~/.hermes/config.yaml` under the Home Assistant platform's `extra` section:
[code] 
    platforms:  
      homeassistant:  
        enabled: true  
        extra:  
          watch_domains:  
            - climate  
            - binary_sensor  
            - alarm_control_panel  
            - light  
          watch_entities:  
            - sensor.front_door_battery  
          ignore_entities:  
            - sensor.uptime  
            - sensor.cpu_usage  
            - sensor.memory_usage  
          cooldown_seconds: 30  
    
[/code]
Setting| Default| Description  
---|---|---  
`watch_domains`|  _(none)_|  Only watch these entity domains (e.g., `climate`, `light`, `binary_sensor`)  
`watch_entities`|  _(none)_|  Only watch these specific entity IDs  
`watch_all`| `false`| Set to `true` to receive **all** state changes (not recommended for most setups)  
`ignore_entities`|  _(none)_|  Always ignore these entities (applied before domain/entity filters)  
`cooldown_seconds`| `30`| Minimum seconds between events for the same entity  
tip
Start with a focused set of domains — `climate`, `binary_sensor`, and `alarm_control_panel` cover the most useful automations. Add more as needed. Use `ignore_entities` to suppress noisy sensors like CPU temperature or uptime counters.
### Event Formatting[​](<#event-formatting> "Direct link to Event Formatting")
State changes are formatted as human-readable messages based on domain:
Domain| Format  
---|---  
`climate`| "HVAC mode changed from 'off' to 'heat' (current: 21, target: 23)"  
`sensor`| "changed from 21°C to 22°C"  
`binary_sensor`| "triggered" / "cleared"  
`light`, `switch`, `fan`| "turned on" / "turned off"  
`alarm_control_panel`| "alarm state changed from 'armed_away' to 'triggered'"  
_(other)_|  "changed from 'old' to 'new'"  
### Agent Responses[​](<#agent-responses> "Direct link to Agent Responses")
Outbound messages from the agent are delivered as **Home Assistant persistent notifications** (via `persistent_notification.create`). These appear in the HA notification panel with the title "Hermes Agent".
### Connection Management[​](<#connection-management> "Direct link to Connection Management")
  * **WebSocket** with 30-second heartbeat for real-time events
  * **Automatic reconnection** with backoff: 5s → 10s → 30s → 60s
  * **REST API** for outbound notifications (separate session to avoid WebSocket conflicts)
  * **Authorization** — HA events are always authorized (no user allowlist needed, since the `HASS_TOKEN` authenticates the connection)


## Security[​](<#security> "Direct link to Security")
The Home Assistant tools enforce security restrictions:
Blocked Domains
The following service domains are **blocked** to prevent arbitrary code execution on the HA host:
  * `shell_command` — arbitrary shell commands
  * `command_line` — sensors/switches that execute commands
  * `python_script` — scripted Python execution
  * `pyscript` — broader scripting integration
  * `hassio` — addon control, host shutdown/reboot
  * `rest_command` — HTTP requests from HA server (SSRF vector)


Attempting to call services in these domains returns an error.
Entity IDs are validated against the pattern `^[a-z_][a-z0-9_]*\.[a-z0-9_]+$` to prevent injection attacks.
## Example Automations[​](<#example-automations> "Direct link to Example Automations")
### Morning Routine[​](<#morning-routine> "Direct link to Morning Routine")
[code] 
    User: Start my morning routine  
      
    Agent:  
    1. ha_call_service(domain="light", service="turn_on",  
         entity_id="light.bedroom", data={"brightness": 128})  
    2. ha_call_service(domain="climate", service="set_temperature",  
         entity_id="climate.thermostat", data={"temperature": 22})  
    3. ha_call_service(domain="media_player", service="turn_on",  
         entity_id="media_player.kitchen_speaker")  
    
[/code]
### Security Check[​](<#security-check> "Direct link to Security Check")
[code] 
    User: Is the house secure?  
      
    Agent:  
    1. ha_list_entities(domain="binary_sensor")  
         → checks door/window sensors  
    2. ha_get_state(entity_id="alarm_control_panel.home")  
         → checks alarm status  
    3. ha_list_entities(domain="lock")  
         → checks lock states  
    4. Reports: "All doors closed, alarm is armed_away, all locks engaged."  
    
[/code]
### Reactive Automation (via Gateway Events)[​](<#reactive-automation-via-gateway-events> "Direct link to Reactive Automation \(via Gateway Events\)")
When connected as a gateway platform, the agent can react to events:
[code] 
    [Home Assistant] Front Door: triggered (was cleared)  
      
    Agent automatically:  
    1. ha_get_state(entity_id="binary_sensor.front_door")  
    2. ha_call_service(domain="light", service="turn_on",  
         entity_id="light.hallway")  
    3. Sends notification: "Front door opened. Hallway lights turned on."  
    
[/code]
  * [Setup](<#setup>)
    * [1\. Create a Long-Lived Access Token](<#1-create-a-long-lived-access-token>)
    * [2\. Configure Environment Variables](<#2-configure-environment-variables>)
    * [3\. Start the Gateway](<#3-start-the-gateway>)
  * [Available Tools](<#available-tools>)
    * [`ha_list_entities`](<#ha_list_entities>)
    * [`ha_get_state`](<#ha_get_state>)
    * [`ha_list_services`](<#ha_list_services>)
    * [`ha_call_service`](<#ha_call_service>)
  * [Gateway Platform: Real-Time Events](<#gateway-platform-real-time-events>)
    * [Event Filtering](<#event-filtering>)
    * [Event Formatting](<#event-formatting>)
    * [Agent Responses](<#agent-responses>)
    * [Connection Management](<#connection-management>)
  * [Security](<#security>)
  * [Example Automations](<#example-automations>)
    * [Morning Routine](<#morning-routine>)
    * [Security Check](<#security-check>)
    * [Reactive Automation (via Gateway Events)](<#reactive-automation-via-gateway-events>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant -->
