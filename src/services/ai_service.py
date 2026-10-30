"""Neonatal Sepsis Monitor AI - Clinical Decision Support System Services Layer.

This module anchors orchestration wrappers for legacy system backwards compatibility,
as well as automated production-grade MLOps monitoring forms utilizing promptfoo.

Author: Dr. Cojocaru & AI Engineering Team
Compliance: PEP 8, PEP 257, Google Python Style Guide, OWASP Top 10
Language: 100% English Codebase & Structural Layouts
"""

import importlib
import logging
import os
import subprocess
from typing import Any

from guardrails.guardrails import NeonatalOutputGuardrail

NeonatalAIExpert = importlib.import_module("medical.expert").NeonatalAIExpert

logger = logging.getLogger(__name__)


class AIService:
    """Legacy wrapper service layout supporting automated backward validation tests.

    Ensures test_ai.py initialization bounds remain intact without altering
    production clinical pipelines.
    """

    def __init__(self) -> None:
        """Initializes the service by mounting the concrete Neonatal AI Expert agent."""
        self.expert: Any = NeonatalAIExpert()
        self.guardrail: NeonatalOutputGuardrail = NeonatalOutputGuardrail()
        self.rag_engine: str = "Legacy Mounted Blueprint Engine"

    def generate_clinical_support(
        self, vitals_payload: dict[str, Any], lang: str
    ) -> str:
        """Routes payload downstream to the verified expert layer and enforces safety guardrails.

        Args:
            vitals_payload (Dict[str, Any]): Multiparametric physiological telemetry coordinates.
            lang (str): Target internationalization language code string.

        Returns:
            str: Structurally validated and self-healed XML clinical prediction sequence.
        """
        raw_output: str = self.expert.generate_clinical_support(
            vitals_payload=vitals_payload, lang=lang
        )

        weight_kg: float = float(
            vitals_payload.get("weight_kg", vitals_payload.get("weight", 2.5))
        )

        _, validated_output = self.guardrail.validate_structure(raw_output)
        self.guardrail.validate_clinical_safety(validated_output, weight_kg=weight_kg)

        return validated_output

    def generate_medical_report(
        self, vitals: dict[str, Any], lang: str, **kwargs: Any
    ) -> str:
        """Legacy routing wrapper mapping directly to the active clinical support layer.

        Satisfies backward compatibility assertions within test_ai.py.

        Args:
            vitals (Dict[str, Any]): Legacy physiological parameter dictionary.
            lang (str): Target language specifier string.
            **kwargs (Any): Additional backward-compatible parameter blocks.

        Returns:
            str: Safe structural clinical evaluation output text.
        """
        return self.generate_clinical_support(vitals_payload=vitals, lang=lang)


class PromptfooOrchestrator:
    """Orchestrates Promptfoo execution and captures evaluation matrix artifacts.

    Runs assertions in mathematical isolation within the persistent venv without blocking
    the user interface threads.
    """

    def __init__(self) -> None:
        """Initializes absolute filesystem paths matching production assets taxonomy."""
        self.base_dir: str = os.getcwd()
        self.report_html: str = os.path.join(
            self.base_dir, "assets", "images", "promptfoo_report.html"
        )
        self.report_csv: str = os.path.join(
            self.base_dir, "assets", "promptfoo_table.csv"
        )

        config_options: list[str] = ["promptfooConfig.yaml", "promptfooconfig.yaml"]
        selected_config: str = "promptfooConfig.yaml"
        for config_file in config_options:
            if os.path.exists(os.path.join(self.base_dir, config_file)):
                selected_config = config_file
                break

        self.config_yaml: str = os.path.join(self.base_dir, selected_config)

    def run_evaluation(self) -> dict[str, Any]:
        """Executes the Promptfoo matrix validation pipeline utilizing production settings.

        Returns:
            Dict[str, Any]: Execution status signature containing success flag and logging output.
        """
        try:
            logger.info(
                "Initializing Promptfoo evaluation from the CDSS console board..."
            )

            command: list[str] = [
                "uv",
                "run",
                "promptfoo",
                "eval",
                "--config",
                self.config_yaml,
                "--no-cache",
                "-o",
                self.report_html,
                "-o",
                self.report_csv,
            ]

            current_env: dict[str, str] = os.environ.copy()
            current_env["NODE_OPTIONS"] = "--no-warnings"

            result: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                env=current_env,
                capture_output=True,
                text=True,
                check=True,
                shell=True,
                encoding="utf-8",
            )

            return {
                "success": True,
                "message": "Evaluation complete! Artifacts successfully generated inside assets/ and images/.",
                "stdout": result.stdout,
            }
        except subprocess.CalledProcessError as e:
            error_msg: str = str(e.stderr if e.stderr else e.stdout)
            logger.error(f"Promptfoo execution routine failed: {error_msg}")

            clean_error: str = error_msg.replace(
                "ExperimentalWarning: DecompressInterceptor is experimental and subject to change",
                "",
            ).strip()
            if not clean_error:
                clean_error = "Check CLI execution pipeline details."

            return {
                "success": False,
                "message": f"Matrix validation failure: {clean_error}",
            }

    def clear_cache(self) -> bool:
        """Purges the local active Promptfoo evaluation cache from the workspace storage.

        Returns:
            bool: True if the cache purge process finished successfully, False otherwise.
        """
        try:
            current_env: dict[str, str] = os.environ.copy()
            current_env["NODE_OPTIONS"] = "--no-warnings"

            subprocess.run(
                ["uv", "run", "promptfoo", "cache", "clear"],
                env=current_env,
                shell=True,
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError:
            logger.error(
                "Failed to clear local Promptfoo diagnostic cache storage bounds."
            )
            return False
