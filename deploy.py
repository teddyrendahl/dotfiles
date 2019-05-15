import argparse
import logging
import os
import pathlib
import sys

logger = logging.getLogger('dotfiles')
EXCLUDED_DOTFILES = ['.git', '.gitsubmodules', '.gitignore']


# Create ArgumentParser
parser = argparse.ArgumentParser()
parser.add_argument('dotfiles', nargs='*',
                    help='Files to create softlinks for. '
                        'If excluded all dotfiles will be included')
parser.add_argument('--output-dir', dest='output_dir', required=False,
                    help='Directory to deploy softlinks. If exclued $HOME will '
                        'be assumed')
parser.add_argument('--log-level', dest='log_level', default='INFO')
parser.add_argument('--overwrite', action='store_true', default=False,
                    help='Flag to overwrite existing softlinks')


if __name__ == '__main__':
    # Parse user input
    args = parser.parse_args(sys.argv[1:])

    # Logging setup
    logging.basicConfig(level=getattr(logging,
                                      args.log_level,
                                      20), # INFO by default
                        format='%(levelname)s - %(message)s')

    # Find install location
    if args.output_dir:
        logger.debug("Using provided output directory %s", args.output_dir)
        output_dir = pathlib.Path(args.output_dir)
    else:
        logger.debug("Searching for $HOME to use as install location")
        output_dir = os.getenv('HOME')
        if not output_dir:
            logger.error("Unable to find install location under "
                         "$HOME. Specify with output-dir")
            sys.exit(1)
        else:
            output_dir = pathlib.Path(output_dir)
    logger.info("Installing dotfiles in %s", output_dir)

    # Create targets
    if args.dotfiles:
        logger.debug("Using user supplied dotfiles %r", args.dotfiles)
        dotfiles = [pathlib.Path(path) for path in args.dotfiles]
    else:
        logger.debug("Searching for dotfiles in current directory")
        dotfiles = ['dotfiles' / pathlib.Path(path)
                    for path in os.listdir('dotfiles')
                    if path.startswith('.')]

    # Create symlinks
    for src in dotfiles:
        dest = output_dir / src.name
        logger.info("Creating symlink %s for %r", dest.absolute(), src.name)
        # Deal with previously existing files
        if dest.exists() or dest.is_symlink():
            logger.info("%s already exists", dest.absolute())
            if args.overwrite:
                logger.warning("Overwriting %s ...", dest)
                dest.unlink()
            else:
                logger.error("Will not replace file. Use '--overwrite'.")
                continue
        try:
            os.symlink(str(src.absolute()), str(dest.absolute()))
        except Exception:
            logger.exception("Unable to create %s", dest)
