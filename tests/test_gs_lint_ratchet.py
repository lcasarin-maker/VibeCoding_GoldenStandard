from scripts import gs_lint


def test_high_audited_without_coverage_fails_ratchet():
    catalogs = {"synthetic.yaml": [{"id": "VC-999", "status": "AUDITED", "severity": "high"}]}
    findings = gs_lint.check_high_audited_coverage(catalogs)
    assert any("VC-999" in finding for finding in findings)


def test_high_audited_with_falsifiable_justification_passes_ratchet():
    catalogs = {"synthetic.yaml": [{
        "id": "VC-999",
        "status": "AUDITED",
        "severity": "high",
        "coverage_justification": "A reproducible test fails when the guard is removed from the source.",
    }]}
    assert gs_lint.check_high_audited_coverage(catalogs) == []


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
