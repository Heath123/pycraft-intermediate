filename = "example.txt"
outfile = "output.txt"

def resolve_data_path(path, nofrom = False):
  args = path.split(" ")
  # inofrom = False
  if args[0] == "from":
    if args[1] == "var":
      args[1] = "storage example:vars"
      return " ".join(args)
  else:
    return path

def parse_line(line):
  # STACK OPERATIONS

  if line.startswith("STACK "): # Initalise stack
    args = line[6:].split(" ")
    return "/data modify storage example:stacks %s set value []\n" % args[0]
  elif line.startswith("PUSH "):
    args = line[5:].split(" ")
    return "/data modify storage example:stacks %s apppend %s\n" % (args[0], " ".join(args[1:]))
  elif line.startswith("POP "):
    args = line[4:].split(" ")
    if len(args) > 2 and args[1] == "TO":
      return "/data modify %s set from storage example:stacks %s[-1]\n" % (resolve_data_path(" ".join(args[2:])), args[0])
    else:
      return "error - no TO\n"

  elif line.startswith("VAR "):
    return "/data modify storage example:vars %s set value 0\n" % line[4:]

  return ""

def parse_file(f, out):
      for line in f:
        if line.startswith("//") or line.strip() == "":
          continue
        elif line.startswith("IMPORT "):
          with open(line[7:].splitlines()[0], "r") as imported:
            parse_file(imported, out)
          continue
        out.write(parse_line(line.splitlines()[0]))

with open(filename, "r") as f:
  with open(outfile, "w") as out:
    parse_file(f, out)