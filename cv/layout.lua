-- Presentation only. All content and company names come from cv.md.
function Pandoc(document)
  local blocks = pandoc.List()
  local company_heading
  local in_experience, role_metadata, technologies = false, false, false
  for index, block in ipairs(document.blocks) do
    local following = document.blocks[index + 1]
    local label = block.t == 'Header' and pandoc.utils.stringify(block.content) or nil
    if technologies and (block.t == 'Para' or block.t == 'Header') then
      -- A missing blank line before --- makes a technology line a Setext H2.
      technologies:insert(pandoc.Str(':'))
      local content = pandoc.List({pandoc.Strong(technologies), pandoc.Space()})
      content:extend(block.content)
      blocks:insert(pandoc.Div({pandoc.Para(content)}, pandoc.Attr('', {'technologies'})))
      technologies = false
    elseif label == 'Professional Experience' and block.level == 2 then
      in_experience = true
      blocks:insert(block)
    elseif label and in_experience and block.level == 2
        and following and following.t == 'Para' and following.content[1]
        and following.content[1].t == 'Strong'
        and pandoc.utils.stringify(following.content[1]):find('|', 1, true) then
      in_experience, role_metadata = true, true
      block.level = 3
      company_heading = block
    elseif label and in_experience and block.level == 3
        and label == 'Key Responsibilities & Achievements' then
      -- The list communicates its purpose without a repeated heading.
    elseif label and in_experience and block.level == 3 and label == 'Technologies' then
      technologies = block.content
    elseif label then
      if block.level <= 2 then in_experience = false end
      blocks:insert(block)
    elseif block.t == 'HorizontalRule' and in_experience then
      -- Company headings provide the visual separation in CSS.
    elseif block.t == 'Para' and role_metadata then
      local role = block.content:remove(1)
      if block.content[1] and block.content[1].t == 'LineBreak' then
        block.content:remove(1)
      end
      blocks:insert(pandoc.Div({company_heading, pandoc.Para({role})},
        pandoc.Attr('', {'experience-heading'})))
      company_heading = nil
      local breaks = 1
      block = block:walk({LineBreak = function()
        breaks = breaks + 1
        if breaks > 1 then return pandoc.Space() end
      end})
      blocks:insert(pandoc.Div({block}, pandoc.Attr('', {'role-metadata'})))
      role_metadata = false
    else
      blocks:insert(block)
    end
  end
  -- Keep each employer's complete description together during pagination.
  local grouped = pandoc.List()
  local entry
  local function flush_entry()
    if entry then
      grouped:insert(pandoc.Div(entry, pandoc.Attr('', {'experience-entry'})))
      entry = nil
    end
  end
  for _, block in ipairs(blocks) do
    if block.t == 'Div' and block.classes:includes('experience-heading') then
      flush_entry()
      entry = pandoc.List({block})
    elseif (block.t == 'Header' and block.level <= 2)
        or (block.t == 'Div' and block.classes:includes('recruitment-clause')) then
      flush_entry()
      grouped:insert(block)
    elseif entry then
      entry:insert(block)
    else
      grouped:insert(block)
    end
  end
  flush_entry()
  document.blocks = grouped
  return document
end
