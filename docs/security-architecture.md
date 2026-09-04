## Security Boundaries

AE-SSS uses strict rules across the Edge and Network levels to keep the system safe, reliable, and secure:

1. **Access Controls:** Operates on a separate, secure network. Devices and Edge nodes use Role-Based Access Control, giving them only the permissions they absolutely need to prevent attackers from moving through the system.
2. **Approved Command Set:** Only allows pre-approved, safe commands to run. The system MUST block and drop any unknown or risky data.
3. **Human-in-the-Loop:** Pauses major automated actions. The system MUST include a mandatory stop rule so human operators can halt any automated process if needed.
4. **Auditability:** Records every piece of sensor data and system action. Real-time logs MUST be kept to ensure complete transparency and accountability.

The system MUST maintain these security rules across all levels. If the network connection drops, Edge nodes MUST keep working safely by saving data locally. They will only sync this data once a secure connection is restored.

## Transport and Agent Constraints

1. **Network Transport:** Uses strong two-way authentication. Every Edge node MUST prove its identity using secure certificates. All data MUST be sent over a highly secure connection, instantly dropping any attempts to use weaker security.
2. **Perception Agent:** Only has permission to read sensor data. It MUST NOT change device settings or network rules.
3. **Edge Intelligence Agent:** Checks local data to evaluate how severe a situation is. It MUST NOT send alerts outside the system or skip safety checks.
4. **Safety and Security Agent:** Runs the approved commands. It MUST check all actions against the system's safety rules before executing them.

All agents MUST follow the standard operating loop of monitor, reason, validate, act, and learn. No agent is allowed to gain extra permissions or bypass the strict network security.

### RAID Log: Edge and Transport Security

* **Type:** Risk
  * **Description:** Attackers might try to connect fake devices to send harmful commands or spam the network.
  * **Mitigation / Resolution:** Use strict certificate authentication (mTLS) so the Secure Broker only accepts data from verified Edge nodes.

* **Type:** Risk
  * **Description:** The AI might misinterpret sensor data and trigger a false emergency alarm.
  * **Mitigation / Resolution:** Enforce a mandatory Human-in-the-Loop (HITL) pause, requiring manual review before any high-impact actions happen.

* **Type:** Assumption
  * **Description:** The Edge device has enough processing power to handle local AI tasks and heavy encryption at the same time.
  * **Mitigation / Resolution:** Run hardware stress tests before full deployment to ensure the device doesn't overheat or lag.

* **Type:** Assumption
  * **Description:** All automated actions can be traced back if something goes wrong.
  * **Mitigation / Resolution:** Continuously log and monitor all agent decisions and network traffic to create a clear audit trail.

* **Type:** Issue
  * **Description:** The 5G or Wi-Fi transport network will occasionally drop, leaving the Edge node disconnected.
  * **Mitigation / Resolution:** Design an offline mode so the Edge node securely stores its data locally and only syncs when the connection returns.

* **Type:** Dependency
  * **Description:** The security boundaries must be clearly documented for the judges to evaluate.
  * **Mitigation / Resolution:** Keep the project specification files updated with all access control rules and network constraints.
