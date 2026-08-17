#!/usr/bin/env python3
"""Inject jailbreak system prompt into Hermes config.yaml - no external deps"""
import os

config_path = os.path.expanduser("~/.hermes/config.yaml")
prompt_path = os.path.expanduser("~/.hermes/system_prompt_jailbreak.md")

# Read the system prompt
with open(prompt_path) as f:
    system_prompt = f.read().strip()

# Read current config
with open(config_path) as f:
    config_content = f.read()

# Check if system_prompt_append already exists
if "system_prompt_append:" in config_content:
    # Find and replace existing value
    import re
    # Match the key and its value (could be multiline)
    pattern = r'system_prompt_append:\s*(.*?)(?=\n\S|\Z)'
    replacement = f"system_prompt_append: |\n" + "\n".join(f"  {line}" for line in system_prompt.split("\n"))
    config_content = re.sub(pattern, replacement, config_content, flags=re.DOTALL)
else:
    # Add after agent: section
    # Find the agent section and add system_prompt_append
    if "agent:" in config_content:
        # Find the agent section and add after it
        lines = config_content.split("\n")
        new_lines = []
        in_agent = False
        agent_indent = 0
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == "agent:" and not in_agent:
                in_agent = True
                agent_indent = len(line) - len(line.lstrip())
                continue
            
            if in_agent and not inserted:
                # Check if next line is at same or lower indent (end of agent section)
                current_indent = len(line) - len(line.lstrip()) if line.strip() else 999
                if current_indent <= agent_indent and line.strip():
                    # We've left the agent section, insert before this line
                    new_lines.pop()  # Remove the current line temporarily
                    prompt_yaml = f"  system_prompt_append: |"
                    for pline in system_prompt.split("\n"):
                        prompt_yaml += f"\n    {pline}"
                    new_lines.append(prompt_yaml)
                    new_lines.append(line)  # Re-add the current line
                    inserted = True
                    in_agent = False
        
        if not inserted:
            # Agent section is at the end, append
            prompt_yaml = f"  system_prompt_append: |"
            for pline in system_prompt.split("\n"):
                prompt_yaml += f"\n    {pline}"
            new_lines.append(prompt_yaml)
        
        config_content = "\n".join(new_lines)

# Write back
with open(config_path, "w") as f:
    f.write(config_content)

print("SUCCESS: system_prompt_append injected into config.yaml")
print(f"Prompt length: {len(system_prompt)} chars")
