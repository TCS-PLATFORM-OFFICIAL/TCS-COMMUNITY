## Summary

<!-- One-sentence description of what this PR does -->

## Type of change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New fetcher (L1 macro / L2 news / L3 sentiment)
- [ ] Improvement to existing fetcher
- [ ] Documentation
- [ ] Tests
- [ ] Other:

## Checklist

- [ ] I have read [CONTRIBUTING.md](../CONTRIBUTING.md) and **agree that my contribution becomes part of TCS-PLATFORM** under the project's MIT license (Contributor License Grant).
- [ ] My code targets **only L1–L3** (data fetching / parsing). No L4–L9 logic.
- [ ] I do NOT include API keys, credentials, or personal data in the diff.
- [ ] I added/updated tests where applicable.
- [ ] I updated `README.md` if I added a new fetcher.
- [ ] The data source I added is publicly accessible and its license permits redistribution.

## How to test

```bash
# Example
pip install -e .
python -m tcs_macro_pulse.fetchers.<your_module> --help
pytest tests/
```

## Related issues

Fixes #
