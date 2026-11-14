-- Presentation only. All content and company names come from cv.md.
function Pandoc(document)
  local blocks = pandoc.List()
  local in_experience, role_metadata, technologies = false, false, false
  for index, block in ipairs(document.blocks) do
    local following = document.blocks[index + 1]
    local label = block.t == 'Header' and pandoc.utils.stringify(block.content) or nil
    if technologies and (block.t == 'Para' or block.t == 'Header') then
      -- A missing blank line before --- makes a technology line a Setext H2.
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
