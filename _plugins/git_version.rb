Jekyll::Hooks.register :site, :after_init do |site|
  # Get git commit count
  commit_count = `git rev-list --count HEAD 2>/dev/null`.strip rescue "0"
  commit_hash = `git rev-parse --short HEAD 2>/dev/null`.strip rescue "unknown"
  commit_date = `git log -1 --format=%cd --date=short 2>/dev/null`.strip rescue Time.now.strftime("%Y-%m-%d")

  # Set default values if git commands fail
  commit_count = "0" if commit_count.nil? || commit_count.empty?
  commit_hash = "unknown" if commit_hash.nil? || commit_hash.empty?
  commit_date = Time.now.strftime("%Y-%m-%d") if commit_date.nil? || commit_date.empty?

  # Add to site config
  site.config['git_version'] = {
    'build_number' => commit_count,
    'commit_hash' => commit_hash,
    'commit_date' => commit_date,
    'version' => "v#{commit_count}"
  }

  puts "Git Version Info: Build ##{commit_count} (#{commit_hash})"
end
