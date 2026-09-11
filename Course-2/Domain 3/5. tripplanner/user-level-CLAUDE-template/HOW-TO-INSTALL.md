# How to set up your USER-LEVEL CLAUDE.md

The `CLAUDE.md` in this folder is a TEMPLATE. To make it your real user-level
memory, it must be copied into your home folder's `.claude` directory.

## Where it goes

    Windows :  C:\Users\<YourName>\.claude\CLAUDE.md
    Mac/Linux: ~/.claude/CLAUDE.md

The `.claude` folder is created automatically when you install Claude Code. The
`CLAUDE.md` file inside it usually does NOT exist yet -- you create it now.

## Option 1 — Let Claude Code create it (easiest)

1. Start Claude Code anywhere:

       claude

2. Type the memory command:

       /memory

3. Choose the USER memory option. Claude Code opens (creating if needed) your
   user-level `CLAUDE.md`. Paste in the contents of the template file, save, and
   close.

## Option 2 — Create it yourself in cmd

From any folder, run these two lines (Windows cmd):

    mkdir "%USERPROFILE%\.claude" 2>nul
    copy "CLAUDE.md" "%USERPROFILE%\.claude\CLAUDE.md"

(The first line makes the `.claude` folder if it isn't there; `2>nul` just hides
the "already exists" message. The second copies this template into place.)

## How to check it worked

Start Claude Code and run `/memory`. Your user-level file should be listed. Open
any project and ask:

    Which CLAUDE.md files are you currently using?

Claude should mention the user-level file no matter which project you are in --
that is what "user-level" means.

## To remove it later

    del "%USERPROFILE%\.claude\CLAUDE.md"
