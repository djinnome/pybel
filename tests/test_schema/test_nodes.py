# -*- coding: utf-8 -*-

"""Unit tests for validating DSL nodes."""

import unittest

from pybel.constants import FUNCTION, NAME, NAMESPACE, PROTEIN, VARIANTS, KIND, MEMBERS, FUSION, PARTNER_3P, PARTNER_5P, RANGE_3P, RANGE_5P
from pybel.dsl import (
    Abundance, BiologicalProcess, ComplexAbundance, Gene, MicroRna, NamedComplexAbundance, Pathology, Protein,
    ProteinModification, Reaction, Rna, ProteinFusion
)
from pybel.schema import validate_node
from pybel.testing.utils import n

HGNC = 'HGNC'
GO = 'GO'
YFG = 'YFG'

phosphorylation = ProteinModification('Ph')
protein_1 = Protein(HGNC, YFG)
protein_2 = Protein(HGNC, YFG, variants=phosphorylation)
rna_1 = Rna(HGNC, YFG)
micro_rna_1 = MicroRna(HGNC, 'YFMR')
gene_1 = Gene(HGNC, YFG)
biological_process_1 = BiologicalProcess(GO, 'YFBP')
pathology_1 = Pathology(GO, 'YFP')
abundance_1 = Abundance(n(), n())
abundance_2 = Abundance(n(), n())
reaction_1 = Reaction(reactants=[abundance_1], products=[abundance_2])
complex_1 = NamedComplexAbundance(n(), n())
enumerated_complex_1 = ComplexAbundance([
    protein_1,
    Protein(HGNC, n()),
])
protein_fusion = ProteinFusion(protein_1, protein_2)

class TestNodeSchema(unittest.TestCase):
    """Tests for the PyBEL node validator."""

    def assertValidNode(self, expr, msg=None):
        """Assert that the node is valid."""
        self.assertTrue(validate_node(expr), msg=msg)

    def assertInvalidNode(self, expr, msg=None):
        """Assert that the node is not valid."""
        self.assertFalse(validate_node(expr), msg=msg)

    def test_simple(self):
        """Test validating simple namespace/name nodes."""
        self.assertValidNode(protein_1, msg="Valid protein, should be validated by schema")
        self.assertValidNode(rna_1)
        self.assertValidNode(micro_rna_1)
        self.assertValidNode(gene_1)
        self.assertValidNode(pathology_1)
        self.assertValidNode(biological_process_1)

    def test_protein_fusion(self):
        """Test validating protein fusion"""
        print(protein_fusion.function, protein_fusion.items())
        self.assertValidNode(protein_fusion)

    def test_reaction(self):
        """Test a reaction."""
        self.assertValidNode(reaction_1)

    def test_enumerated_complex(self):
        """Test a enumareted complex."""
        print('Log> ', enumerated_complex_1.function)
        self.assertValidNode(enumerated_complex_1)

    def test_enumerated_complex_fail(self):
        """Test a complex with invalid properties"""
        self.assertInvalidNode({
            NAME: 'YFC',
            FUNCTION: 'Complex',
            MEMBERS: [],
            VARIANTS: [
                { KIND: 'pmod' }
            ]
        }, msg="Complex with invalid properties should fail")

    def test_pathology_fail(self):
        """Test a pathway with invalid properties, should fail"""
        self.assertInvalidNode({
            NAME: 'YFP',
            FUNCTION: 'Pathology',
            NAMESPACE: GO,
            MEMBERS: [],
            FUSION: {
                PARTNER_5P: protein_1,
                PARTNER_3P: protein_2,
            }
        }, msg="Should fail because two invalid properties")

    def test_simple_fail(self):
        """Test validating simple namespace/name nodes."""
        self.assertInvalidNode({
            NAMESPACE: 'HGNC',
            NAME: 'YFG',
        }, msg='Invalid object, should not be validated')

    def test_protein_with_modification(self):
        """Test validating a protein with modifications."""
        self.assertValidNode(protein_2, msg="Valid protein, should be validated by schema")

    def test_protein_with_modification_fail(self):
        """Test invalidating a protein with modifications that are incorrect"""
        test_protein = {
            FUNCTION: PROTEIN,
            NAMESPACE: 'HGNC',
            NAME: 'YFG',
            VARIANTS: [
                {
                    # KIND: 'pmod'
                }
            ],
        }
        self.assertInvalidNode(test_protein, msg="Invalid protein with mods, should not be validated by schema")