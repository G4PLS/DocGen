---@module Pain
--@author g4pls
---

---@hook DTTTHandleMute
--@author g4pls
--@realm a
--@desc Handles all Mute Logic. Runs on %hook:TTT2PostPlayerDeath%
--@param Player ply
--@param boolean state Mute state
--@param number duration Duration mute state should last
---
function GM:DTTTHandleMute()
end

---@hook DTTTPreMute
--@author g4pls
--@realm server
--@desc Runs bevor actual mute logic happens in %hook:DTTTHandleMute%
--@param Player ply Player to mute
--@param boolean state Mute state
--@param number duration Duration mute state should last
--@return boolean false To stop execution
--@return table {ply, state, duration} to modify the values
--@return nil nil To just continue execution
---
function GM:DTTTPreMute()
end

---@hook DTTTMute
--@realm shared
--@desc Runs actual mute logic. Gets called by %hook:DTTTHandleMute%
--@param Player ply Player to mute
--@param boolean state Mute state
--@param number duration Duration mute state should last
--@return boolean false To stop execution
--@return table {ply, state, duration} to modify the values
--@return nil To just continue execution
---
function GM:DTTTMute()
end


---@convar ttt_idle_limit
--@default number 5
--@desc Help text
--@flags FCVAR_NOTIFY FCVAR_ARCHIVE
---
local idle_time = CreateConVar("ttt_idle_limit", "180", { FCVAR_NOTIFY, FCVAR_ARCHIVE }, "Help text")