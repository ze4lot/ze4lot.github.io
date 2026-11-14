-- Layout transformations only: approved Markdown remains untouched.
-- cv.md may contain experience inline (current source), or select it by link.
function Pandoc(document)
  local file = assert(io.open('cv/experience.md', 'r'))
  local markdown = file:read('*a')
  file:close()
  local experience = pandoc.read(markdown, 'markdown-smart')
  local companies = {}
  for _, block in ipairs(experience.blocks) do
    if block.t == 'Header' and block.level == 2 then
      companies[pandoc.utils.stringify(block.content)] = true
    end
  end

  local expanded = pandoc.List()
  for _, block in ipairs(document.blocks) do
    if block.t == 'Para' and #block.content == 1
        and block.content[1].t == 'Link' and block.content[1].target == 'experience.md' then
      for index, entry in ipairs(experience.blocks) do
        if not (index == 1 and entry.t == 'Header' and entry.level == 1) then
          expanded:insert(entry)
        end
      end
    else
      expanded:insert(block)
    end
  end

  local blocks = pandoc.List()
  local in_experience, role_metadata, technologies = false, false, false
  for _, block in ipairs(expanded) do
    local label = block.t == 'Header' and pandoc.utils.stringify(block.content) or nil
    if technologies and (block.t == 'Para' or block.t == 'Header') then
      -- A missing blank line before --- makes a technology line a Setext H2.
      local content = pandoc.List({pandoc.Strong(technologies), pandoc.Space()})
      content:extend(block.content)
      blocks:insert(pandoc.Div({pandoc.Para(content)}, pandoc.Attr('', {'technologies'})))
      technologies = false
    elseif label and block.level == 2 and companies[label] then
      in_experience, role_metadata = true, true
      block.level = 3
      blocks:insert(block)
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
      local breaks = 0
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
  document.blocks = blocks
  return document
end
