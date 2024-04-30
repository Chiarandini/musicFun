--  ╔══════════════════════════════════════════════════════════╗
--  ║                       programming                        ║
--  ╚══════════════════════════════════════════════════════════╝

return {
	-- for suggested code compltion
	-- NOTE: COSTS MONEY WITHOUT STUDENT ENTERPRISE GITHUB
	-- {
	-- 	"zbirenbaum/copilot.lua",
	-- 	cmd = "Copilot",
	-- 	event = "InsertEnter",
	-- 	config = function()
	-- 		require("copilot").setup({})
	-- 	end,
	-- },
	{
		-- context-smart comment construction
		"danymat/neogen",
		keys = {
			{
				"<Leader>c",
				function()
					require("neogen").generate({})
				end,
				desc = "add comment",
				{ noremap = true, silent = true },
			},
		},
		dependencies = "nvim-treesitter/nvim-treesitter",
		config = function()
			require("neogen").setup({
				snippet_engine = "luasnip",
			})
		end,
		-- Uncomment next line if you want to follow only stable versions
		-- version = "*"
	},
	-- better around/in operators
	{ "echasnovski/mini.ai",    version = false },

	-- better quick fix
	{
		"kevinhwang91/nvim-bqf",
		ft = "qf",
	},

	{ "CRAG666/betterTerm.nvim" },

	--visuzlize progress of multiple tasks
	-- NOTE: under development, version='legacy' introduced to avoid breaking setup
	-- NOTE: Noice has it's own fidget-like functionality; disabling this for now
	{
		"j-hui/fidget.nvim",
		event = "VeryLazy",
		config = function()
			require("fidget").setup({})
		end,
	},

	--to make it easier to see indentation
	{
		"lukas-reineke/indent-blankline.nvim",
		event = "VeryLazy",
		config = function()
			require("ibl").setup()
		end
	},

	{ -- to explain regex in floating window
		"tomiis4/Hypersonic.nvim",
		event = "CmdlineEnter",
		cmd = "Hypersonic",
		config = function()
			require("hypersonic").setup({
				-- disable regexing for / and ?
				enable_cmdline = false,
			})
		end,
	},
	{ -- highlight same variable
		"RRethy/vim-illuminate",
		-- event = { "VeryLazy" },
		cmd = { "IlluminateResumeBuf", "IlluminatePauseBuf" },
		config = function()
			require("configs.illuminate")
		end,
	},
	-- NOTE: commented for now since not using TMUX
	{ -- for tmux-integration
		'christoomey/vim-tmux-navigator'
	},

	{ -- show what colour a hex code in neovim gives. Don't forget :ColorizerToggle
		"norcalli/nvim-colorizer.lua",
		ft = { "lua", "html", "css", "python" },
		cmd = { "ColorizerToggle" },
		config = function()
			require("colorizer").setup({
				lua = {
					mode = "foreground", --options: foreground, background
				},
			})
		end,
	},

	-- for color picking
	{
		"uga-rosa/ccc.nvim",
		cmd = { "CccPick" },
		config = function ()
			require('ccc').setup()
		end
	},

	{ -- forbetter refactoring. Read README for interaction with debugging.
		"ThePrimeagen/refactoring.nvim",
		cmd = "Refactor",
		keys = {
			{ "<leader>re",  ":Refactor extract ",              mode = "x",          desc = "extract" },
			{ "<leader>rf",  ":Refactor extract_to_file ",      mode = "x",          desc = "extract to file" },
			{ "<leader>rv",  ":Refactor extract_var ",          mode = "x",          desc = "extract var" },
			{ "<leader>ri",  ":Refactor inline_var",            mode = { "n", "x" }, desc = "inline var" },
			{ "<leader>rb",  ":Refactor extract_block",         mode = "n",          desc = "extract block" },
			{ "<leader>rbf", ":Refactor extract_block_to_file", mode = "n",          desc = "block to file" },
		},
		config = true,
	},
	{ -- to visualize dense code blocks
		"HampusHauffman/block.nvim",
		cmd = { "Block", "BlockOn", "BlockOff" },
		config = true,
	},
	-- minimap
	{
		"echasnovski/mini.map",
		version = false,
		keys = {
			{
				"[om",
				function()
					MiniMap.open()
				end,
				desc = "open minimap",
			},
			{
				"]om",
				function()
					MiniMap.close()
				end,
				desc = "open minimap",
			},
		},
		config = function()
			require("mini.map").setup()
		end,
	},
	{ -- for vaf, ]m/[m, and so much more! Should really learn more
		"nvim-treesitter/nvim-treesitter-textobjects",
		event = {'InsertEnter', 'BufReadPost'},
		config = function()
			require('configs.treesitter-objects')
---@diagnostic disable-next-line: missing-fields
			end,
	},
	{
		'rafcamlet/nvim-luapad',
		cmd = 'Luapad',
		config = function()
			require('luapad').setup()
		end
	},
	{
		"willothy/flatten.nvim",
		config = true,
		event = 'TermOpen',
		-- or pass configuration with
		-- opts = {  }
		-- Ensure that it runs first to minimize delay when opening file from terminal
		priority = 1001,
	},
	{ -- for jupyter notebooks
		"luk400/vim-jukit",
		keys = "<leader>np",
	},
-- WARN: This looks really cool, but couldn't get it to work
	-- { -- run python blocks
	-- 	"dccsillag/magma-nvim",
	-- 	build = ":UpdateRemotePlugins",
	-- 	keys = {
	-- 		{"<LocalLeader>r",  "<cmd>MagmaEvaluateOperator<CR>"   , mode="n"},
	-- 		{"<LocalLeader>rr", "<cmd>MagmaEvaluateLine<CR>"       , mode="n"},
	-- 		{"<LocalLeader>r",  "<cmd><C-u>MagmaEvaluateVisual<CR>", mode="x"},
	-- 		{"<LocalLeader>rc", "<cmd>MagmaReevaluateCell<CR>"     , mode="n"},
	-- 		{"<LocalLeader>rd", "<cmd>MagmaDelete<CR>"             , mode="n"},
	-- 		{"<LocalLeader>ro", "<cmd>MagmaShowOutput<CR>"         , mode="n"},
	-- 	},
	-- },

	{ -- REPL code
		"Vigemus/iron.nvim",
		keys = {
			{'<leader>rs', '<cmd>IronRepl<cr>'},
			{'<leader>rr', '<cmd>IronRestart<cr>'},
			{'<leader>rf', '<cmd>IronFocus<cr>'},
			{'<leader>rh', '<cmd>IronHide<cr>'},
		},
		config = function()
			require('configs.iron')
		end
	}
	-- TODO: wanna decide what I wanna keep
	-- {
	-- more bracket options
	--    "echasnovski/mini.bracketed",
	--    event = "BufReadPost",
	--    config = function()
	-- 	require("mini.bracketed").setup({
	-- 		buffer = { suffix = 'B', options = {} }, -- [b and ]b is for tab switching
	-- 	})
	-- end
	-- },

	--to visually see quick-fix actions
	-- {
	-- 	"kosayoda/nvim-lightbulb",
	-- 	event = "InsertEnter", --User ActuallyEditing
	-- 	dependencies = "antoinemadec/FixCursorHold.nvim",
	-- 	config = function()
	-- 		require("nvim-lightbulb").setup({ autocmd = { enabled = true } })
	-- 	end,
	-- },

	-- preffered in-vim terminal

	-- crumbs on side to show erros and warning
	-- ISSUE: currently requires version 0.10.0
	-- {
	-- 	'lewis6991/satellite.nvim',
	-- 	event = "VeryLazy",
	-- 	config = function()
	-- 		require("satellite").setup()
	-- 	end,
	-- },
	-- NOTE: I don't really use this, so commented for now
	-- {
	-- 	'dstein64/nvim-scrollview',
	-- 	configuration = function()
	-- 		require('scrollview').setup({
	-- 			excluded_filetypes = { 'nerdtree' },
	-- 			current_only = true,
	-- 			base = 'buffer',
	-- 			column = 80,
	-- 			signs_on_startup = { 'all' },
	-- 			diagnostics_severities = { vim.diagnostic.severity.ERROR }
	-- 		})
	-- 	end
	-- }
}
