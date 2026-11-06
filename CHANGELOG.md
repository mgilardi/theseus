# Changelog

## Unreleased
- **The iMessage channel can only answer in your own self-chat.** The send guard now checks where each reply is going, and refuses anything else even if the plugin's allowlist would permit it.
- **Runs clear their scratch files.** Hidden temporary exports, like a copy of your Reminders, are removed when a run ends.
- **Release builds are harder to tamper with.** GitHub Actions are pinned to exact commits, the signing secrets reach only the step that needs them, and the write token isn't left where an install script could use it.

## 0.6.0
- **Unattended runs have firmer limits.** Texts, email and web pages are treated as data, never instructions. Runs nobody is watching can't search the web or change your settings, and no session can read your SSH, cloud or signing keys, or your Claude login.
- **No copies of your messages stay behind.** The copies of Messages, Contacts and Mail are deleted when each run ends, and stay out of Time Machine. Your workspace is now private to your account. A Claude Code session without Full Disk Access can no longer read texts from an old copy, and it says so.
- **`theseus undo`.** Takes back your last `add` or `done`, until the next sync.
- **The send guard catches more names.** Tools named like `sendMessage` or `REPLYALL` are refused.
- **The Remote Control log stays small.** It's capped at 5 MB, and the app no longer reads the whole file when the server restarts.
- **Fixed two bugs reported by Matt Abate:** underscores disappearing from names in the Today view, and search hits losing their marker.
- **Shorter commands.** They're now one word, and three no longer share a name with a Claude Code command. `/status` is `/refresh`, `/review` is `/weekly`, `/voice` is `/tone`, `/thread-report` is `/report`, `/text-research` is `/research`, `/sync-check` is `/history`, and `/compliance-check` is `/compliance`. Updating removes the old names, so `/status`, `/review` and `/voice` now reach Claude Code's own commands.
- **A list of every command.** Run `/commands` in a session, or `theseus help` in Terminal.
- **More from Terminal, without Claude.** `theseus today` prints your Today note, `theseus done "bank"` checks off what matches, and `theseus texts` shows who's waiting on a reply.
- **In the app.** Activity shows your thread notes, read-only, and Setup lists every command.
- **Thread notes, when you ask.** `/learn Sam` keeps deep, neutral notes on how you and Sam talk. It reads only messages the notes haven't covered, and logs every check, including the ones that change nothing.
- **An outside read, when you ask.** `/mirror Sam` gives an unbiased opinion on how you come across in that conversation, with dated examples.

## 0.5.3
- **A new icon and color.** Theseus is now a compass on seafoam, with a deep teal accent inside the app. Ariadne gets a matching change.

## 0.5.2
- **A `theseus` command, alongside `ariadne`.** `theseus` opens a chat in Terminal, and `theseus "a question"` asks one thing. `theseus status`, `next` and `add` are instant and don't use Claude. `theseus sync` and `morning` run the real job and print the result. It all uses the same workspace, rules and send guard as the app. Installing or updating the engine links it at `~/.local/bin/theseus`.
- **One run at a time.** The app, the schedule and the command now share a lock, so a sync you start by hand can't overlap one that's already running. A scheduled briefing waits its turn.
- **Shannon is on the roadmap as an idea only.** Theseus and Ariadne stay separate apps. See `docs/ROADMAP.md`.

## 0.5.1
- **Just open the app.** Once its permissions are in place, Theseus moves everything into the app by itself, with no click and without Claude or Terminal open. Until then its window opens and says what's missing. Handing back to Terminal stays handed back until you choose otherwise.
- **ClickUp and Skylight sync on their own again.** Unattended runs can make the updates a sync needs: updating a ClickUp task, and adding, updating and completing Skylight chores, tasks and list items. Sending is still refused, and deleting still needs you.

## 0.5.0
Everything from a full review of the app and engine. App, engine and plugin now share one version number.

**Never sends, enforced**
- The send guard now covers every connector, not just Composio, in every session. A write hiding behind a read word (`FIND_OR_CREATE`, `LIST_ADD_MEMBER`) no longer counts as a read, and if the guard can't decide, the call is blocked instead of going ahead.
- **Unattended runs only read ClickUp, Skylight and other connectors.** They used to be able to send ClickUp messages and delete Skylight items. Changing something now needs a live session, or you can allow one exact tool in `.claude/settings.local.json`. `--update` moves existing workspaces over.

**Nothing lost**
- A detected change stays on the books until its sync finishes, so a failed or skipped run is retried instead of waiting for the hourly refresh.
- What you do in the app reaches the next sync only once it's saved, and anything you do during a sync waits for the next one (`engine/tools/app_edits.py`). Completing something in the Markdown view now counts.
- `config.json` and `state.json` are written whole, under a lock where two programs share them. Taking over no longer reorders `config.json`.
- If a sync lands while you're typing, what you typed is saved in `data/archive`, and undo can't overwrite the sync.
- Reopening a checked-off item puts it back in the section it came from. Items with the same title no longer get mixed up.
- A slow Notes app no longer looks like a deleted note, so it can't create a duplicate Today note or lose your pin.
- Contact names work in Claude Code sessions again, using the saved copies.
- Theseus's own Today note update no longer starts another run every 15 minutes.
- The list note's counts stay right, and failures to update it are shown.

**Running from the app**
- A briefing missed while the Mac slept runs when it wakes. Restarting doesn't send it twice, and an evening run set after midnight fires on the right night.
- A run that hangs is stopped after 45 minutes (`job_time_limit_minutes`), under launchd too.
- Theseus opens at login and reopens after a crash, once it hosts. Quitting from the menu bar is respected.
- Taking over stops only this workspace's Remote Control server, not other projects', changes the config first so a failure can't strand you, and leaves the iMessage channel running.
- Both hosts share prompts, log cleanup and opening helper apps. Logging out stops Remote Control cleanly.
- **Releases are signed with a stable certificate, so updates keep your macOS permissions.** This release asks for them one last time.
- The app warns when the engine doesn't match it, finds a workspace that isn't `~/Theseus` when opened from Finder, and checks for Apple's command line tools.

**The window**
- Renaming a section no longer makes its block disappear. Your answer stays when a later run finishes. A drag released outside the window ends, and closing the window finishes any check-off in its countdown. Old list backups are removed after 14 days.

**Installer and tests**
- `--update` now reaches the scripts launchd runs, and no longer re-adds connectors you took out.
- New: `tests/test_engine.py` and browser tests of the window in `apps/desktop/e2e`, both run by CI, plus a check that files shared with Ariadne stay identical. CI's leak check can use your private terms through the `LEAK_TERMS` secret.

## Before 0.5.0
- **Edit your list in the app.** A new List page, and live Now and Communication blocks on Today, both working on `data/master.md`. Drag to reorder or move between sections, double-click to rename, or switch to a raw Markdown view. It saves as you go, with undo and redo (⌘Z, ⇧⌘Z) and an hourly backup in `data/archive`. A sync that changes the file at the same time is merged, not overwritten.
- **Checking something off** gives you three seconds to change your mind, then it moves to Done. Repeating items stay put, marked done for now.
- The next sync carries what you did to Reminders, Skylight and ClickUp, and treats your drags as your own ranking instead of re-sorting them (`data/app-edits.jsonl`, RULES §3).
- Icons instead of emoji throughout the app, and a softer, pastel app icon.
- **Calendar permission fixed.** The app was built with Apple's hardened runtime and no calendar entitlement, so macOS refused silently: no dialog, and that pane has no + button. Reminders has no such gate, which is why it worked.
- **New interface and icon.** A sidebar with Today, Activity and Setup; the Today note laid out as a real page; ask Theseus from the app; shared design system with Ariadne (`brand/README.md`). The icon is now a Greek key unwinding into a straight line.
- **Setup** shows each permission's real state without prompting, and never freezes the window while a dialog is up.
- **Hosting:** taking over stops the old jobs first and explains the wait while the old server lets go. Handing back restarts the background jobs right away, instead of leaving nothing running.
- **Email in unattended runs:** connector detection missed every `claude.ai` connector, so Composio was never allowed. Fixed, with `engine/tools/send_guard.py` refusing anything that sends or deletes, and holding anything that isn't a plain read for a person to approve.
- New identity: an Athenian ship in ivory on Aegean blue, a monochrome menu bar icon that follows light and dark mode, and matching colors in the app.
- **Theseus for Mac is available** from Releases, built automatically. Every push now runs CI: leak check, script and Python checks, and an app build.
- **Ariadne is a separate tool** (ADR 0005). Theseus doesn't move files. With `integrations.ariadne` on, a check-in offers a filing pass when `ariadne count` passes `checkin_offers.unfiled`.
- **Theseus.app (M1 scaffold):** menu bar app in `apps/desktop` that hosts Remote Control, change checks and morning/nightly runs under one set of macOS permissions; Today / Services / Permissions views; "Take over hosting". `run-job.sh` stands down when `scheduler_host` is `app`. See ADR 0006.
- **Remote Control now runs in a Terminal window by default** (`remote_control.host: "terminal"`), kept open by a background watchdog.
  Terminal is then the app in charge, so phone sessions get its permissions, like command-line runs. `"background"` and a future `"app"` mode remain.
- **Remote Control server fixes**: input held open with a FIFO (it quit on "end of input" under launchd), a clean stop on restart (no leftover
  server blocking the next one with "already served"), and leftovers stopped before starting.
- **Texts and Mail inside Claude Code sessions**: when macOS blocks direct reads there, the tools fall back to saved copies, which the
  5-minute checks (running from /bin/bash, which has access) refresh whenever texts or mail change.
- `--schedule` now also (1) allows your connected MCP servers in scheduled runs via `.claude/settings.local.json` (Slack excluded, since it can
  post), and (2) runs `--grant`: a one-off background job that makes macOS ask for Calendar, Reminders and Notes access *for the background jobs*,
  which don't inherit Terminal's permissions. Removed invalid `Write(...)` permission rules (Edit rules cover all file edits).
- README: "Lightly opinionated": a fresh install starts blank and learns the person; the only fixed requirement is a Mac that stays on.
- **Always reachable**: `--schedule` now also keeps a Claude Code **Remote Control** server running in the workspace (`remote_control`, on by
  default; `--remote` installs it alone). The Mac appears in the Claude app's Code tab, so a fresh Theseus session can be started from anywhere.
  It restarts after crashes, reboots and `--update`, and nightly and morning health checks flag it in the Today note if it's down.
- **Text Theseus from your phone** (optional): `engine/install.sh --channel` keeps an iMessage channel session running in the workspace
  (official plugin; self-chat only; restarts after crashes and daily for new rules; removed by `--unschedule`). Setup step, docs §6b, compliance A8.
- `repeating_tasks_in_master` (default true): set false to keep repeating Reminders out of the master list; they still show under ⏰ when due.
  `lists_outside_master` keeps whole Reminders lists out.
- `extra_sections`: add your own master list sections (e.g. 💬 COMMUNICATIONS after NOW). Existing unknown sections are never dropped.
- Groceries by store (`grocery_reminders_list` as a list, mapped to Skylight sections), optional chore ⇄ Reminder sync (`chore_reminder_sync`,
  `data/chore-map.json`), and a rule for changing a chore's schedule without erasing its history.
- **Backlog check-in offers** (RULES §7d): one optional, timed "Got 5 minutes?" offer when a backlog builds up, at natural moments only,
  with yes / later / not today / never answers, and learning when the user likes to tidy. Thresholds in `config.checkin_offers`.
- **README rewritten**: who it's for, how it tailors itself, bubble-sort ranking up front, every command, how to start, roadmap, and an
  integrations table with one service per line (email and calendar listed separately per provider), with links and support status.
- **MCP vs Composio** explained: use either, or both, per service. Email and calendar accounts each carry their own `source`.
- **Slack, two ways**: the official Slack MCP connector (Claude Code sign-in, read-only use) or the email bridge. Setup asks which provider gets
  the notifications and gives step-by-step filters for Gmail/Google Workspace, Outlook/Microsoft 365 and iCloud.
- **Repeating reminders**: `ek add-reminder` and `ek update` take `--recur "<RRULE>"`, `ek update` takes `--clear-recur`, and reminder output
  includes `recurrence`.
- Repeating tasks in the rules: one repeating Reminder plus one `↻` master item; completing an occurrence keeps the item and advances its due date
  instead of moving it to DONE. A plain-language → RRULE table, and a confirmation the first time.
- `recurrence` in reminder output is now built from the rule's own fields (stable across macOS versions); safer BYSETPOS parsing.
- `install.sh` flags work in any order (`--force --update` == `--update --force`).
- docs/SETUP.md §10a explains the local-changes handoff for contributors.
- **Local changes handoff**: `data/local-changes.md` records engine changes made or recommended in a workspace (`engine/tools/local_changes.py`).
  A SessionStart hook in this repo lists pending entries, and `install` and `--update` stop if a pending patch isn't in the source (`--force` overrides).

## 0.4.0
- **Flexible schedules**: regimented or fluid, weekday/weekend (or any) day groups, single-day overrides, flex hours. Morning and nightly runs
  are scheduled per day (including evening runs after midnight). A "you're up" refresh fires on the first activity after 4+ quiet hours, and
  weekly rhythm learning suggests schedule tweaks. Setup now asks about all of this. (`engine/tools/schedule.py`)
- **docs/APP-PLAN.md**: plan for Theseus.app as a single shipped package (Tauri 2, same engine), milestones M0–M5.
- Architecture decision records in `docs/adr`.

## 0.3.1
- Local checks can run every few minutes (default 5). Claude is rate-limited (`min_minutes_between_claude_runs`, default 15), and changes
  seen during the wait are queued. Awake hours are enforced in the check itself. The Notes app is no longer launched on every check.

## 0.3.0
- **Configurable frequent checks** (`checks` in config.json; default every 30 min while awake, opt-in). A local change test
  (`engine/tools/changes.py`) runs first, and Claude only runs if texts, notes, reminders, calendar, alarms or mail changed, or a full refresh is due.
  Replaces `hourly_sync`.

## 0.2.0
- 📌 Pinned **Today** note, republished on every run. It works offline, and your edits (✍️ Jot here, ☐→x, reordering) are read back.
  🌙 Tomorrow is now a section of it instead of a separate note.
- Philosophy written into the rules: Theseus helps you live your life; it doesn't live it for you.
- Docs: running unsigned preview builds of the planned Mac app; the two ways an app can talk to Claude.
- CREDITS.md and the borrowing policy.
- Monthly **compliance check**: re-reads Anthropic's rules against docs/COMPLIANCE.md and proposes changes (it never edits on its own).
- README: free and open source, always.
- Scheduled runs quietly open any apps listed in `ensure_apps` (plus Apple Mail when it's the email source).

## 0.1.0
- First public version: master list (NOW/NEXT/LATER/EVENTUALLY), Notes inbox, nightly "🌙 Tomorrow" and morning "☀️ Today" briefings,
  texts-waiting, as-if-they-asked reply drafting, pairwise ranking, "what's next?" check-ins, auto-detection of done items,
  thread reports, iPhone alarms via Shortcuts, Things 3 migration, optional Skylight / ClickUp / Slack email bridge.
- Email and calendar from connectors (e.g. Composio) or Apple Mail / Calendar, chosen per user.
