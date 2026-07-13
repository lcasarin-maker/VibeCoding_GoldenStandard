from scripts import gs_lint


def test_high_doc_only_without_falsifiable_justification_fails_ratchet():
    catalogs = {"synthetic.yaml": [{"id": "VC-999", "status": "DOC_ONLY", "severity": "high"}]}
    findings = gs_lint.check_high_doc_only_justification(catalogs)
    assert any("VC-999" in finding for finding in findings)


def test_high_doc_only_with_falsifiable_justification_passes_ratchet():
    catalogs = {"synthetic.yaml": [{
        "id": "VC-999",
        "status": "DOC_ONLY",
        "severity": "high",
        "doc_only_justification": "Promote only after a positive fixture, negative fixture, and CI-enforced gate exist.",
    }]}
    assert gs_lint.check_high_doc_only_justification(catalogs) == []


def test_evidence_classification_is_closed_set():
    catalogs = {"synthetic.yaml": [{
        "id": "VC-999",
        "evidence": [
            {"source": "https://example.test/primary", "claim": "primary"},
            {"source": "Internal report, cited generically", "claim": "internal"},
            {"source": "PENDING: source to be located", "claim": "pending"},
        ],
    }]}
    assert gs_lint.check_evidence_classification(catalogs) == []


def test_live_catalogs_have_no_transitional_audited_status():
    assert gs_lint.check_no_audited_statuses() == []


def test_transitional_status_is_rejected(tmp_path):
    catalog = tmp_path / "golden_standard_synthetic.yaml"
    catalog.write_text(
        "items:\n- id: VC-999\n  title: Synthetic\n  status: " + gs_lint.LEGACY_REVIEW_STATUS + "\n",
        encoding="utf-8",
    )
    findings = gs_lint.check_no_audited_statuses(tmp_path)
    assert any("VC-999" in finding for finding in findings)


def test_static_mechanism_without_fixtures_fails_gate():
    catalogs = {
        "synthetic.yaml": [
            {"id": "VC-999", "validating_mechanism": "static-ast", "example_bad": "", "example_good": ""},
        ]
    }
    findings = gs_lint.check_code_mechanism_requires_fixtures(catalogs)
    assert any("VC-999" in finding for finding in findings)


def test_static_mechanism_with_fixtures_passes_gate():
    catalogs = {
        "synthetic.yaml": [
            {
                "id": "VC-999",
                "validating_mechanism": "static-regex",
                "example_bad": "eval(x)  # nosemgrep",
                "example_good": "eval(x)  # nosemgrep: id -- reason",
            },
        ]
    }
    assert gs_lint.check_code_mechanism_requires_fixtures(catalogs) == []


def test_doctrinal_mechanism_is_exempt_from_fixture_gate():
    catalogs = {
        "synthetic.yaml": [
            {"id": "PR-999", "validating_mechanism": "doctrinal", "example_bad": "", "example_good": ""},
        ]
    }
    assert gs_lint.check_code_mechanism_requires_fixtures(catalogs) == []
