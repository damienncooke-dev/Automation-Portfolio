resource "local_file" "change_state" {
  filename = "demofile.txt"
  content  = "Demo file to force a state file to be generated."
}
