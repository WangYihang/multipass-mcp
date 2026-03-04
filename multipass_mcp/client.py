import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)


class MultipassError(Exception):
    """Base exception for Multipass errors."""


class InstanceNotFoundError(MultipassError):
    """Raised when an instance is not found."""


class MultipassCLI:
    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout

    async def _run(self, *args: str) -> str:
        logger.debug(f"Running Multipass command: multipass {' '.join(args)}")
        try:
            process = await asyncio.wait_for(
                asyncio.create_subprocess_exec(
                    'multipass',
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                ),
                timeout=self.timeout,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(
                    f"Multipass error (exit {process.returncode}): {error_msg}",
                )
                raise MultipassError(f"Multipass error: {error_msg}")

            return stdout.decode().strip()
        except TimeoutError:
            logger.error(f"Multipass command timed out: {' '.join(args)}")
            raise MultipassError(f"Command timed out after {self.timeout}s")
        except Exception as e:
            if not isinstance(e, MultipassError):
                logger.exception('Unexpected error running Multipass command')
            raise
