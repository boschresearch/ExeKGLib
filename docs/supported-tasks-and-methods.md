🗒️ **Note**: Parent tasks are marked with 📜. Only bottom-level tasks (marked with ☑️) can be used while creating a pipeline.

<details>
	<summary>Train 📜<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>Regression 📜</summary>
			<ul>
				<details>
					<summary>BayesianRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>ARDRegressionMethod</summary>
								<ul>
									<li>hasParamAlpha1 (float)</li>
									<li>hasParamAlpha2 (float)</li>
									<li>hasParamComputeScore (boolean)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLambda1 (float)</li>
									<li>hasParamLambda2 (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIter (int)</li>
									<li>hasParamThresholdLambda (float)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>BayesianRidgeMethod</summary>
								<ul>
									<li>hasParamAlpha1 (float)</li>
									<li>hasParamAlpha2 (float)</li>
									<li>hasParamAlphaInit (float)</li>
									<li>hasParamComputeScore (boolean)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLambda1 (float)</li>
									<li>hasParamLambda2 (float)</li>
									<li>hasParamLambdaInit (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIter (int)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>BoostingRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>AdaBoostRegressorMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>GradientBoostingRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamInit (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSubsample (float, int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>HistGradientBoostingRegressorMethod</summary>
								<ul>
									<li>hasParamCategoricalFeatures (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamInteractionCst (int, string)</li>
									<li>hasParamL2Regularization (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxBins (int)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMonotonicCst (string)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamQuantile (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>DecisionTreeRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>DecisionTreeRegressorMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreeRegressorMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>InstanceBasedRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>KNeighborsRegressorMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamNNeighbors (int)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>RadiusNeighborsRegressorMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamRadius (float)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>LeastAngleRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>LarsMethod</summary>
								<ul>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamFitPath (boolean)</li>
									<li>hasParamJitter (float)</li>
									<li>hasParamNNonzeroCoefs (int)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LassoLarsMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamFitPath (boolean)</li>
									<li>hasParamJitter (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>RandomForestRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>ExtraTreesRegressorMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RandomForestRegressorMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>RegularizedRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>BaggingRegressorMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamBootstrapFeatures (boolean)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>ElasticNetCVMethod</summary>
								<ul>
									<li>hasParamAlphas (string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNAlphas (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>ElasticNetMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>GammaRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>HuberRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>LarsCVMethod</summary>
								<ul>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxNAlphas (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LassoCVMethod</summary>
								<ul>
									<li>hasParamAlphas (string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNAlphas (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LassoLarsCVMethod</summary>
								<ul>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxNAlphas (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LassoLarsICMethod</summary>
								<ul>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNoiseVariance (float)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LassoMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>MLPRegressorMethod</summary>
								<ul>
									<li>hasParamActivation (string)</li>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamBatchSize (int)</li>
									<li>hasParamBeta1 (float)</li>
									<li>hasParamBeta2 (float)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLearningRateInit (float)</li>
									<li>hasParamMaxFun (int)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMomentum (float)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNesterovsMomentum (boolean)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>MultiTaskElasticNetCVMethod</summary>
								<ul>
									<li>hasParamAlphas (string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNAlphas (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>MultiTaskElasticNetMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>MultiTaskLassoCVMethod</summary>
								<ul>
									<li>hasParamAlphas (string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEps (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNAlphas (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>MultiTaskLassoMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSelection (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>OneClassSVMMethod</summary>
								<ul>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNu (float)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OrthogonalMatchingPursuitCVMethod</summary>
								<ul>
									<li>hasParamCopy (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OrthogonalMatchingPursuitMethod</summary>
								<ul>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamNNonzeroCoefs (int)</li>
									<li>hasParamPrecompute (boolean, string)</li>
									<li>hasParamTol (float, string)</li>
								</ul>
							</details>
							<details>
								<summary>PassiveAggressiveRegressorMethod</summary>
								<ul>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamC (float)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>PoissonRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>QuantileRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamQuantile (float)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamSolverOptions (string)</li>
								</ul>
							</details>
							<details>
								<summary>RANSACRegressorMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamIsDataValid (string)</li>
									<li>hasParamIsModelValid (string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxSkips (int)</li>
									<li>hasParamMaxTrials (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamResidualThreshold (float)</li>
									<li>hasParamStopNInliers (int)</li>
									<li>hasParamStopScore (float)</li>
								</ul>
							</details>
							<details>
								<summary>RidgeCVMethod</summary>
								<ul>
									<li>hasParamAlphaPerTarget (boolean)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamGcvMode (string)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamStoreCvValues (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RidgeMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
								</ul>
							</details>
							<details>
								<summary>SGDOneClassSVMMethod</summary>
								<ul>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamEta0 (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNu (float)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>SGDRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamEta0 (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>StackingRegressorMethod</summary>
								<ul>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEstimators (string)</li>
									<li>hasParamFinalEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPassthrough (boolean)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>TheilSenRegressorMethod</summary>
								<ul>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxSubpopulation (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamNSubsamples (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>TweedieRegressorMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLink (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPower (float)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>VotingRegressorMethod</summary>
								<ul>
									<li>hasParamEstimators (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>SimpleRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>LinearRegressionMethod</summary>
								<ul>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPositive (boolean)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>SupportVectorRegression ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>LinearSVRMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>NuSVRMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNu (float)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>SVRMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>Classification 📜</summary>
			<ul>
				<details>
					<summary>BinaryClassification ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>AdaBoostClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>BaggingClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamBootstrapFeatures (boolean)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>BernoulliNBMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamBinarize (float, string)</li>
									<li>hasParamFitPrior (boolean)</li>
									<li>hasParamForceAlpha (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>BernoulliRBMMethod</summary>
								<ul>
									<li>hasParamBatchSize (int)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamNComponents (float, int, string)</li>
									<li>hasParamNIter (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>CategoricalNBMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitPrior (boolean)</li>
									<li>hasParamForceAlpha (boolean)</li>
									<li>hasParamMinCategories (int)</li>
								</ul>
							</details>
							<details>
								<summary>ComplementNBMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitPrior (boolean)</li>
									<li>hasParamForceAlpha (boolean)</li>
									<li>hasParamNorm (boolean, string)</li>
								</ul>
							</details>
							<details>
								<summary>DecisionTreeClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreeClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreesClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>GaussianNBMethod</summary>
								<ul>
									<li>hasParamVarSmoothing (float)</li>
								</ul>
							</details>
							<details>
								<summary>GradientBoostingClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamInit (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSubsample (float, int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>HistGradientBoostingClassifierMethod</summary>
								<ul>
									<li>hasParamCategoricalFeatures (string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamInteractionCst (int, string)</li>
									<li>hasParamL2Regularization (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxBins (int)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMonotonicCst (string)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>KNeighborsClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamNNeighbors (int)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>LinearSVCMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMultiClass (string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LogisticRegressionCVMethod</summary>
								<ul>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCs (int, string)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamL1Ratios (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMultiClass (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamRefit (boolean)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LogisticRegressionMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMultiClass (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>MLPClassifierMethod</summary>
								<ul>
									<li>hasParamActivation (string)</li>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamBatchSize (int)</li>
									<li>hasParamBeta1 (float)</li>
									<li>hasParamBeta2 (float)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLearningRateInit (float)</li>
									<li>hasParamMaxFun (int)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMomentum (float)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNesterovsMomentum (boolean)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>MultinomialNBMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamFitPrior (boolean)</li>
									<li>hasParamForceAlpha (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>NearestCentroidMethod</summary>
								<ul>
									<li>hasParamMetric (string)</li>
									<li>hasParamShrinkThreshold (float)</li>
								</ul>
							</details>
							<details>
								<summary>NuSVCMethod</summary>
								<ul>
									<li>hasParamBreakTies (boolean)</li>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDecisionFunctionShape (string)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNu (float)</li>
									<li>hasParamProbability (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OneVsOneClassifierMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>OneVsRestClassifierMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OutputCodeClassifierMethod</summary>
								<ul>
									<li>hasParamCodeSize (float)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>PassiveAggressiveClassifierMethod</summary>
								<ul>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamC (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>PerceptronMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEta0 (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RadiusNeighborsClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOutlierLabel (string)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamRadius (float)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>RandomForestClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RidgeClassifierCVMethod</summary>
								<ul>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamStoreCvValues (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RidgeClassifierMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
								</ul>
							</details>
							<details>
								<summary>SGDClassifierMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamEta0 (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>SVCMethod</summary>
								<ul>
									<li>hasParamBreakTies (boolean)</li>
									<li>hasParamC (float)</li>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDecisionFunctionShape (string)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamProbability (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>StackingClassifierMethod</summary>
								<ul>
									<li>hasParamCv (int, string)</li>
									<li>hasParamEstimators (string)</li>
									<li>hasParamFinalEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPassthrough (boolean)</li>
									<li>hasParamStackMethod (string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>VotingClassifierMethod</summary>
								<ul>
									<li>hasParamEstimators (string)</li>
									<li>hasParamFlattenTransform (boolean)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamVoting (string)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>MulticlassClassification ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>AdaBoostClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>BernoulliNBMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamBinarize (float, string)</li>
									<li>hasParamFitPrior (boolean)</li>
									<li>hasParamForceAlpha (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>DecisionTreeClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreeClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreesClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>GaussianNBMethod</summary>
								<ul>
									<li>hasParamVarSmoothing (float)</li>
								</ul>
							</details>
							<details>
								<summary>GradientBoostingClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamInit (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSubsample (float, int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>HistGradientBoostingClassifierMethod</summary>
								<ul>
									<li>hasParamCategoricalFeatures (string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamInteractionCst (int, string)</li>
									<li>hasParamL2Regularization (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxBins (int)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMonotonicCst (string)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>KNeighborsClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamNNeighbors (int)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>LinearSVCMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMultiClass (string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LogisticRegressionCVMethod</summary>
								<ul>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCs (int, string)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamL1Ratios (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMultiClass (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamRefit (boolean)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>LogisticRegressionMethod</summary>
								<ul>
									<li>hasParamC (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamDual (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamInterceptScaling (float)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMultiClass (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>MLPClassifierMethod</summary>
								<ul>
									<li>hasParamActivation (string)</li>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamBatchSize (int)</li>
									<li>hasParamBeta1 (float)</li>
									<li>hasParamBeta2 (float)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLearningRateInit (float)</li>
									<li>hasParamMaxFun (int)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMomentum (float)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNesterovsMomentum (boolean)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>NearestCentroidMethod</summary>
								<ul>
									<li>hasParamMetric (string)</li>
									<li>hasParamShrinkThreshold (float)</li>
								</ul>
							</details>
							<details>
								<summary>NuSVCMethod</summary>
								<ul>
									<li>hasParamBreakTies (boolean)</li>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDecisionFunctionShape (string)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNu (float)</li>
									<li>hasParamProbability (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OneVsOneClassifierMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>OneVsRestClassifierMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OutputCodeClassifierMethod</summary>
								<ul>
									<li>hasParamCodeSize (float)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>PassiveAggressiveClassifierMethod</summary>
								<ul>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamC (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>PerceptronMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEta0 (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RadiusNeighborsClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOutlierLabel (string)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamRadius (float)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>RandomForestClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RidgeClassifierCVMethod</summary>
								<ul>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCv (int, string)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamStoreCvValues (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>RidgeClassifierMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCopyX (boolean)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamPositive (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSolver (string)</li>
									<li>hasParamTol (float, string)</li>
								</ul>
							</details>
							<details>
								<summary>SGDClassifierMethod</summary>
								<ul>
									<li>hasParamAlpha (float, int, string)</li>
									<li>hasParamAverage (boolean, int, string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamEpsilon (float)</li>
									<li>hasParamEta0 (float)</li>
									<li>hasParamFitIntercept (boolean)</li>
									<li>hasParamL1Ratio (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamPenalty (string)</li>
									<li>hasParamPowerT (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShuffle (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>SVCMethod</summary>
								<ul>
									<li>hasParamBreakTies (boolean)</li>
									<li>hasParamC (float)</li>
									<li>hasParamCacheSize (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCoef0 (float)</li>
									<li>hasParamDecisionFunctionShape (string)</li>
									<li>hasParamDegree (float, int, string)</li>
									<li>hasParamGamma (float, string)</li>
									<li>hasParamKernel (string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamProbability (boolean)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamShrinking (boolean)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
				<details>
					<summary>MultilabelClassification ☑️</summary>
					<ul>
						<details>
							<summary>Inputs</summary>
							<ul>
								<li>DataInTrainX</li>
								<li>DataInTrainY</li>
							</ul>
						</details>
						<details>
							<summary>Outputs</summary>
							<ul>
								<li>DataOutTrainModel</li>
							</ul>
						</details>
						<details>
							<summary>Methods</summary>
							<ul>
							<details>
								<summary>AdaBoostClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>DecisionTreeClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreeClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSplitter (string)</li>
								</ul>
							</details>
							<details>
								<summary>ExtraTreesClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>GradientBoostingClassifierMethod</summary>
								<ul>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamInit (string)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamSubsample (float, int, string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>HistGradientBoostingClassifierMethod</summary>
								<ul>
									<li>hasParamCategoricalFeatures (string)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamEarlyStopping (boolean)</li>
									<li>hasParamInteractionCst (int, string)</li>
									<li>hasParamL2Regularization (float)</li>
									<li>hasParamLearningRate (float, string)</li>
									<li>hasParamLoss (string)</li>
									<li>hasParamMaxBins (int)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxIter (int)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMonotonicCst (string)</li>
									<li>hasParamNIterNoChange (int)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamScoring (string)</li>
									<li>hasParamTol (float, string)</li>
									<li>hasParamValidationFraction (float, int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							<details>
								<summary>KNeighborsClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamNNeighbors (int)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>OneVsOneClassifierMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>OneVsRestClassifierMethod</summary>
								<ul>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
								</ul>
							</details>
							<details>
								<summary>OutputCodeClassifierMethod</summary>
								<ul>
									<li>hasParamCodeSize (float)</li>
									<li>hasParamEstimator (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamRandomState (int, string)</li>
								</ul>
							</details>
							<details>
								<summary>RadiusNeighborsClassifierMethod</summary>
								<ul>
									<li>hasParamAlgorithm (string)</li>
									<li>hasParamLeafSize (int)</li>
									<li>hasParamMetric (string)</li>
									<li>hasParamMetricParams (string)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOutlierLabel (string)</li>
									<li>hasParamP (float, int)</li>
									<li>hasParamRadius (float)</li>
									<li>hasParamWeights (string)</li>
								</ul>
							</details>
							<details>
								<summary>RandomForestClassifierMethod</summary>
								<ul>
									<li>hasParamBootstrap (boolean)</li>
									<li>hasParamCcpAlpha (float)</li>
									<li>hasParamClassWeight (string)</li>
									<li>hasParamCriterion (string)</li>
									<li>hasParamMaxDepth (int, string)</li>
									<li>hasParamMaxFeatures (float, int, string)</li>
									<li>hasParamMaxLeafNodes (int, string)</li>
									<li>hasParamMaxSamples (float, int)</li>
									<li>hasParamMinImpurityDecrease (float)</li>
									<li>hasParamMinSamplesLeaf (float, int)</li>
									<li>hasParamMinSamplesSplit (float, int)</li>
									<li>hasParamMinWeightFractionLeaf (float)</li>
									<li>hasParamNEstimators (int)</li>
									<li>hasParamNJobs (int, string)</li>
									<li>hasParamOobScore (boolean, string)</li>
									<li>hasParamRandomState (int, string)</li>
									<li>hasParamVerbose (boolean, int)</li>
									<li>hasParamWarmStart (boolean)</li>
								</ul>
							</details>
							</ul>
						</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>Clustering ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInTrainX</li>
						<li>DataInTrainY</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutTrainModel</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>AffinityPropagationMethod</summary>
						<ul>
							<li>hasParamAffinity (string)</li>
							<li>hasParamConvergenceIter (int)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamDamping (float)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamPreference (float)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>AgglomerativeClusteringMethod</summary>
						<ul>
							<li>hasParamComputeDistances (boolean)</li>
							<li>hasParamComputeFullTree (boolean)</li>
							<li>hasParamConnectivity (string)</li>
							<li>hasParamDistanceThreshold (float)</li>
							<li>hasParamLinkage (string)</li>
							<li>hasParamMemory (string)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamNClusters (int, string)</li>
						</ul>
					</details>
					<details>
						<summary>BirchMethod</summary>
						<ul>
							<li>hasParamBranchingFactor (int)</li>
							<li>hasParamComputeLabels (boolean)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamThreshold (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>BisectingKMeansMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamBisectingStrategy (string)</li>
							<li>hasParamCopyX (boolean)</li>
							<li>hasParamInit (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamNInit (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>DBSCANMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamEps (float)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamMinSamples (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamP (float, int)</li>
						</ul>
					</details>
					<details>
						<summary>HDBSCANMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamAllowSingleCluster (boolean)</li>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamClusterSelectionEpsilon (float)</li>
							<li>hasParamClusterSelectionMethod (string)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMaxClusterSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamMinClusterSize (int)</li>
							<li>hasParamMinSamples (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamStoreCenters (string)</li>
						</ul>
					</details>
					<details>
						<summary>IsolationForestMethod</summary>
						<ul>
							<li>hasParamBootstrap (boolean)</li>
							<li>hasParamContamination (float)</li>
							<li>hasParamMaxFeatures (float, int, string)</li>
							<li>hasParamMaxSamples (float, int)</li>
							<li>hasParamNEstimators (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
							<li>hasParamWarmStart (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>KMeansMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamCopyX (boolean)</li>
							<li>hasParamInit (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamNInit (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>KNeighborsTransformerMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamMode (string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamP (float, int)</li>
						</ul>
					</details>
					<details>
						<summary>KernelDensityMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamAtol (float)</li>
							<li>hasParamBandwidth (float, string)</li>
							<li>hasParamBreadthFirst (boolean)</li>
							<li>hasParamKernel (string)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamRtol (float)</li>
						</ul>
					</details>
					<details>
						<summary>LocalOutlierFactorMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamContamination (float)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamNovelty (boolean)</li>
							<li>hasParamP (float, int)</li>
						</ul>
					</details>
					<details>
						<summary>MeanShiftMethod</summary>
						<ul>
							<li>hasParamBandwidth (float, string)</li>
							<li>hasParamBinSeeding (boolean)</li>
							<li>hasParamClusterAll (boolean)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMinBinFreq (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamSeeds (string)</li>
						</ul>
					</details>
					<details>
						<summary>MiniBatchKMeansMethod</summary>
						<ul>
							<li>hasParamBatchSize (int)</li>
							<li>hasParamComputeLabels (boolean)</li>
							<li>hasParamInit (string)</li>
							<li>hasParamInitSize (int)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMaxNoImprovement (int, string)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamNInit (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamReassignmentRatio (float)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>NearestNeighborsMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamRadius (float)</li>
						</ul>
					</details>
					<details>
						<summary>OPTICSMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamClusterMethod (string)</li>
							<li>hasParamEps (float)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMaxEps (float)</li>
							<li>hasParamMemory (string)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamP (float, int)</li>
							<li>hasParamPredecessorCorrection (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>RadiusNeighborsTransformerMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamLeafSize (int)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMetricParams (string)</li>
							<li>hasParamMode (string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamP (float, int)</li>
							<li>hasParamRadius (float)</li>
						</ul>
					</details>
					<details>
						<summary>SpectralBiclusteringMethod</summary>
						<ul>
							<li>hasParamInit (string)</li>
							<li>hasParamMethod (string)</li>
							<li>hasParamMiniBatch (boolean)</li>
							<li>hasParamNBest (int)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNInit (int)</li>
							<li>hasParamNSvdVecs (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamSvdMethod (string)</li>
						</ul>
					</details>
					<details>
						<summary>SpectralClusteringMethod</summary>
						<ul>
							<li>hasParamAffinity (string)</li>
							<li>hasParamAssignLabels (string)</li>
							<li>hasParamCoef0 (float)</li>
							<li>hasParamDegree (float, int, string)</li>
							<li>hasParamEigenSolver (string)</li>
							<li>hasParamEigenTol (float)</li>
							<li>hasParamGamma (float, string)</li>
							<li>hasParamKernelParams (string)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNInit (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>SpectralCoclusteringMethod</summary>
						<ul>
							<li>hasParamInit (string)</li>
							<li>hasParamMiniBatch (boolean)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamNInit (int)</li>
							<li>hasParamNSvdVecs (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamSvdMethod (string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>Concatenation ☑️<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>Inputs</summary>
			<ul>
				<li>DataInConcatenation</li>
			</ul>
		</details>
		<details>
			<summary>Outputs</summary>
			<ul>
				<li>DataOutConcatenatedData</li>
			</ul>
		</details>
		<details>
			<summary>Methods</summary>
			<ul>
			<details>
				<summary>ConcatenationMethod</summary>
				<ul>No parameters</ul>
			</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>PrepareTransformer 📜<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>DataProcessing ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPrepareTransformer</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutTransformer</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>BinarizerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamThreshold (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>DictVectorizerMethod</summary>
						<ul>
							<li>hasParamDtype (string)</li>
							<li>hasParamSeparator (string)</li>
							<li>hasParamSort (boolean)</li>
							<li>hasParamSparse (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>FeatureHasherMethod</summary>
						<ul>
							<li>hasParamAlternateSign (boolean)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamInputType (string)</li>
							<li>hasParamNFeatures (int)</li>
						</ul>
					</details>
					<details>
						<summary>FunctionTransformerMethod</summary>
						<ul>
							<li>hasParamAcceptSparse (boolean)</li>
							<li>hasParamCheckInverse (boolean)</li>
							<li>hasParamFeatureNamesOut (string)</li>
							<li>hasParamFunc (string)</li>
							<li>hasParamInvKwArgs (string)</li>
							<li>hasParamInverseFunc (string)</li>
							<li>hasParamKwArgs (string)</li>
							<li>hasParamValidate (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>KBinsDiscretizerMethod</summary>
						<ul>
							<li>hasParamDtype (string)</li>
							<li>hasParamEncode (string)</li>
							<li>hasParamNBins (int)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamStrategy (string)</li>
							<li>hasParamSubsample (float, int, string)</li>
						</ul>
					</details>
					<details>
						<summary>KNNImputerMethod</summary>
						<ul>
							<li>hasParamAddIndicator (boolean)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamKeepEmptyFeatures (boolean)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamMissingValues (float, int, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamWeights (string)</li>
						</ul>
					</details>
					<details>
						<summary>KernelCentererMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>LabelBinarizerMethod</summary>
						<ul>
							<li>hasParamNegLabel (int)</li>
							<li>hasParamPosLabel (boolean, float, int, string)</li>
							<li>hasParamSparseOutput (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>MaxAbsScalerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>MinMaxScalerMethod</summary>
						<ul>
							<li>hasParamClip (boolean)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamFeatureRange (string)</li>
						</ul>
					</details>
					<details>
						<summary>MissingIndicatorMethod</summary>
						<ul>
							<li>hasParamErrorOnNew (boolean)</li>
							<li>hasParamFeatures (string)</li>
							<li>hasParamMissingValues (float, int, string)</li>
							<li>hasParamSparse (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>MultiLabelBinarizerMethod</summary>
						<ul>
							<li>hasParamSparseOutput (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>NormalizerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamNorm (boolean, string)</li>
						</ul>
					</details>
					<details>
						<summary>OneHotEncoderMethod</summary>
						<ul>
							<li>hasParamCategories (string)</li>
							<li>hasParamDrop (string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamFeatureNameCombiner (string)</li>
							<li>hasParamHandleUnknown (string)</li>
							<li>hasParamMaxCategories (int)</li>
							<li>hasParamMinFrequency (float, int)</li>
							<li>hasParamSparseOutput (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>OrdinalEncoderMethod</summary>
						<ul>
							<li>hasParamCategories (string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamEncodedMissingValue (int, string)</li>
							<li>hasParamHandleUnknown (string)</li>
							<li>hasParamMaxCategories (int)</li>
							<li>hasParamMinFrequency (float, int)</li>
							<li>hasParamUnknownValue (int, string)</li>
						</ul>
					</details>
					<details>
						<summary>PolynomialFeaturesMethod</summary>
						<ul>
							<li>hasParamDegree (float, int, string)</li>
							<li>hasParamIncludeBias (boolean)</li>
							<li>hasParamInteractionOnly (boolean)</li>
							<li>hasParamOrder (string)</li>
						</ul>
					</details>
					<details>
						<summary>PowerTransformerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamMethod (string)</li>
							<li>hasParamStandardize (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>QuantileTransformerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamIgnoreImplicitZeros (boolean)</li>
							<li>hasParamNQuantiles (int)</li>
							<li>hasParamOutputDistribution (string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamSubsample (float, int, string)</li>
						</ul>
					</details>
					<details>
						<summary>RandomTreesEmbeddingMethod</summary>
						<ul>
							<li>hasParamMaxDepth (int, string)</li>
							<li>hasParamMaxLeafNodes (int, string)</li>
							<li>hasParamMinImpurityDecrease (float)</li>
							<li>hasParamMinSamplesLeaf (float, int)</li>
							<li>hasParamMinSamplesSplit (float, int)</li>
							<li>hasParamMinWeightFractionLeaf (float)</li>
							<li>hasParamNEstimators (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamSparseOutput (boolean)</li>
							<li>hasParamVerbose (boolean, int)</li>
							<li>hasParamWarmStart (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>RobustScalerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamQuantileRange (string)</li>
							<li>hasParamUnitVariance (boolean)</li>
							<li>hasParamWithCentering (boolean)</li>
							<li>hasParamWithScaling (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>SimpleImputerMethod</summary>
						<ul>
							<li>hasParamAddIndicator (boolean)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamFillValue (string)</li>
							<li>hasParamKeepEmptyFeatures (boolean)</li>
							<li>hasParamMissingValues (float, int, string)</li>
							<li>hasParamStrategy (string)</li>
						</ul>
					</details>
					<details>
						<summary>SplineTransformerMethod</summary>
						<ul>
							<li>hasParamDegree (float, int, string)</li>
							<li>hasParamExtrapolation (string)</li>
							<li>hasParamIncludeBias (boolean)</li>
							<li>hasParamKnots (string)</li>
							<li>hasParamNKnots (int)</li>
							<li>hasParamOrder (string)</li>
							<li>hasParamSparseOutput (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>StandardScalerMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamWithMean (boolean)</li>
							<li>hasParamWithStd (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>TargetEncoderMethod</summary>
						<ul>
							<li>hasParamCategories (string)</li>
							<li>hasParamCv (int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamShuffle (boolean)</li>
							<li>hasParamSmooth (float)</li>
							<li>hasParamTargetType (string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>Decomposition ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPrepareTransformer</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutTransformer</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>DictionaryLearningMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamCallback (string)</li>
							<li>hasParamCodeInit (string)</li>
							<li>hasParamDictInit (string)</li>
							<li>hasParamFitAlgorithm (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamPositiveCode (boolean)</li>
							<li>hasParamPositiveDict (boolean)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamSplitSign (boolean)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamTransformAlgorithm (string)</li>
							<li>hasParamTransformAlpha (float)</li>
							<li>hasParamTransformMaxIter (int)</li>
							<li>hasParamTransformNNonzeroCoefs (int)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>FactorAnalysisMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamIteratedPower (int)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamRotation (string)</li>
							<li>hasParamSvdMethod (string)</li>
							<li>hasParamTol (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>FastICAMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamFun (string)</li>
							<li>hasParamFunArgs (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamWInit (string)</li>
							<li>hasParamWhiten (boolean, string)</li>
							<li>hasParamWhitenSolver (string)</li>
						</ul>
					</details>
					<details>
						<summary>FeatureAgglomerationMethod</summary>
						<ul>
							<li>hasParamComputeDistances (boolean)</li>
							<li>hasParamComputeFullTree (boolean)</li>
							<li>hasParamConnectivity (string)</li>
							<li>hasParamDistanceThreshold (float)</li>
							<li>hasParamLinkage (string)</li>
							<li>hasParamMemory (string)</li>
							<li>hasParamMetric (string)</li>
							<li>hasParamNClusters (int, string)</li>
							<li>hasParamPoolingFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>IncrementalPCAMethod</summary>
						<ul>
							<li>hasParamBatchSize (int)</li>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamWhiten (boolean, string)</li>
						</ul>
					</details>
					<details>
						<summary>KernelPCAMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamCoef0 (float)</li>
							<li>hasParamCopyX (boolean)</li>
							<li>hasParamDegree (float, int, string)</li>
							<li>hasParamEigenSolver (string)</li>
							<li>hasParamFitInverseTransform (boolean)</li>
							<li>hasParamGamma (float, string)</li>
							<li>hasParamKernel (string)</li>
							<li>hasParamKernelParams (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamRemoveZeroEig (boolean)</li>
							<li>hasParamTol (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>LatentDirichletAllocationMethod</summary>
						<ul>
							<li>hasParamBatchSize (int)</li>
							<li>hasParamDocTopicPrior (float)</li>
							<li>hasParamEvaluateEvery (int)</li>
							<li>hasParamLearningDecay (float)</li>
							<li>hasParamLearningMethod (string)</li>
							<li>hasParamLearningOffset (float)</li>
							<li>hasParamMaxDocUpdateIter (int)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMeanChangeTol (float)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamPerpTol (float)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTopicWordPrior (float)</li>
							<li>hasParamTotalSamples (int)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>MiniBatchDictionaryLearningMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamBatchSize (int)</li>
							<li>hasParamCallback (string)</li>
							<li>hasParamDictInit (string)</li>
							<li>hasParamFitAlgorithm (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMaxNoImprovement (int, string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamPositiveCode (boolean)</li>
							<li>hasParamPositiveDict (boolean)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamShuffle (boolean)</li>
							<li>hasParamSplitSign (boolean)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamTransformAlgorithm (string)</li>
							<li>hasParamTransformAlpha (float)</li>
							<li>hasParamTransformMaxIter (int)</li>
							<li>hasParamTransformNNonzeroCoefs (int)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>MiniBatchNMFMethod</summary>
						<ul>
							<li>hasParamAlphaH (float)</li>
							<li>hasParamAlphaW (float)</li>
							<li>hasParamBatchSize (int)</li>
							<li>hasParamBetaLoss (float, string)</li>
							<li>hasParamForgetFactor (float)</li>
							<li>hasParamFreshRestarts (boolean)</li>
							<li>hasParamFreshRestartsMaxIter (int)</li>
							<li>hasParamInit (string)</li>
							<li>hasParamL1Ratio (float)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMaxNoImprovement (int, string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamTransformMaxIter (int)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>MiniBatchSparsePCAMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamBatchSize (int)</li>
							<li>hasParamCallback (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMaxNoImprovement (int, string)</li>
							<li>hasParamMethod (string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamRidgeAlpha (float)</li>
							<li>hasParamShuffle (boolean)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>NMFMethod</summary>
						<ul>
							<li>hasParamAlphaH (float)</li>
							<li>hasParamAlphaW (float)</li>
							<li>hasParamBetaLoss (float, string)</li>
							<li>hasParamInit (string)</li>
							<li>hasParamL1Ratio (float)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamShuffle (boolean)</li>
							<li>hasParamSolver (string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>NeighborhoodComponentsAnalysisMethod</summary>
						<ul>
							<li>hasParamCallback (string)</li>
							<li>hasParamInit (string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamVerbose (boolean, int)</li>
							<li>hasParamWarmStart (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>PCAMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamIteratedPower (int)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNOversamples (int)</li>
							<li>hasParamPowerIterationNormalizer (string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamSvdSolver (string)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamWhiten (boolean, string)</li>
						</ul>
					</details>
					<details>
						<summary>SparseCoderMethod</summary>
						<ul>
							<li>hasParamDictionary (string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamPositiveCode (boolean)</li>
							<li>hasParamSplitSign (boolean)</li>
							<li>hasParamTransformAlgorithm (string)</li>
							<li>hasParamTransformAlpha (float)</li>
							<li>hasParamTransformMaxIter (int)</li>
							<li>hasParamTransformNNonzeroCoefs (int)</li>
						</ul>
					</details>
					<details>
						<summary>SparsePCAMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamMaxIter (int)</li>
							<li>hasParamMethod (string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamRidgeAlpha (float)</li>
							<li>hasParamTol (float, string)</li>
							<li>hasParamUInit (string)</li>
							<li>hasParamVInit (string)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>TruncatedSVDMethod</summary>
						<ul>
							<li>hasParamAlgorithm (string)</li>
							<li>hasParamNComponents (float, int, string)</li>
							<li>hasParamNIter (int)</li>
							<li>hasParamNOversamples (int)</li>
							<li>hasParamPowerIterationNormalizer (string)</li>
							<li>hasParamRandomState (int, string)</li>
							<li>hasParamTol (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>FeatureSelection ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPrepareTransformer</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutTransformer</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>Chi2Method</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>FClassifMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>FRegressionMethod</summary>
						<ul>
							<li>hasParamCenter (boolean)</li>
							<li>hasParamForceFinite (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>GenericUnivariateSelectMethod</summary>
						<ul>
							<li>hasParamMode (string)</li>
							<li>hasParamParam (float, int)</li>
							<li>hasParamScoreFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>MutualInfoClassifMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamDiscreteFeatures (boolean, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamRandomState (int, string)</li>
						</ul>
					</details>
					<details>
						<summary>MutualInfoRegressionMethod</summary>
						<ul>
							<li>hasParamCopy (boolean)</li>
							<li>hasParamDiscreteFeatures (boolean, string)</li>
							<li>hasParamNNeighbors (int)</li>
							<li>hasParamRandomState (int, string)</li>
						</ul>
					</details>
					<details>
						<summary>RFECVMethod</summary>
						<ul>
							<li>hasParamCv (int, string)</li>
							<li>hasParamEstimator (string)</li>
							<li>hasParamImportanceGetter (string)</li>
							<li>hasParamMinFeaturesToSelect (int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamScoring (string)</li>
							<li>hasParamStep (float, int)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>RFEMethod</summary>
						<ul>
							<li>hasParamEstimator (string)</li>
							<li>hasParamImportanceGetter (string)</li>
							<li>hasParamNFeaturesToSelect (float, int)</li>
							<li>hasParamStep (float, int)</li>
							<li>hasParamVerbose (boolean, int)</li>
						</ul>
					</details>
					<details>
						<summary>SelectFdrMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamScoreFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>SelectFprMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamScoreFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>SelectFromModelMethod</summary>
						<ul>
							<li>hasParamEstimator (string)</li>
							<li>hasParamImportanceGetter (string)</li>
							<li>hasParamMaxFeatures (float, int, string)</li>
							<li>hasParamNormOrder (int, string)</li>
							<li>hasParamPrefit (boolean)</li>
							<li>hasParamThreshold (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>SelectFweMethod</summary>
						<ul>
							<li>hasParamAlpha (float, int, string)</li>
							<li>hasParamScoreFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>SelectKBestMethod</summary>
						<ul>
							<li>hasParamK (int)</li>
							<li>hasParamScoreFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>SelectPercentileMethod</summary>
						<ul>
							<li>hasParamPercentile (int)</li>
							<li>hasParamScoreFunc (string)</li>
						</ul>
					</details>
					<details>
						<summary>SequentialFeatureSelectorMethod</summary>
						<ul>
							<li>hasParamCv (int, string)</li>
							<li>hasParamDirection (string)</li>
							<li>hasParamEstimator (string)</li>
							<li>hasParamNFeaturesToSelect (float, int)</li>
							<li>hasParamNJobs (int, string)</li>
							<li>hasParamScoring (string)</li>
							<li>hasParamTol (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>VarianceThresholdMethod</summary>
						<ul>
							<li>hasParamThreshold (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>DataSplitting ☑️<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>Inputs</summary>
			<ul>
				<li>DataInDataSplittingX</li>
				<li>DataInDataSplittingY</li>
			</ul>
		</details>
		<details>
			<summary>Outputs</summary>
			<ul>
				<li>DataOutSplittedTestDataX</li>
				<li>DataOutSplittedTestDataY</li>
				<li>DataOutSplittedTrainDataX</li>
				<li>DataOutSplittedTrainDataY</li>
			</ul>
		</details>
		<details>
			<summary>Methods</summary>
			<ul>
			<details>
				<summary>CheckCvMethod</summary>
				<ul>
					<li>hasParamClassifier (boolean)</li>
					<li>hasParamCv (int, string)</li>
				</ul>
			</details>
			<details>
				<summary>CrossValPredictMethod</summary>
				<ul>
					<li>hasParamCv (int, string)</li>
					<li>hasParamEstimator (string)</li>
					<li>hasParamFitParams (string)</li>
					<li>hasParamMethod (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamParams (string)</li>
					<li>hasParamPreDispatch (int, string)</li>
					<li>hasParamVerbose (boolean, int)</li>
				</ul>
			</details>
			<details>
				<summary>CrossValScoreMethod</summary>
				<ul>
					<li>hasParamCv (int, string)</li>
					<li>hasParamErrorScore (string)</li>
					<li>hasParamFitParams (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamParams (string)</li>
					<li>hasParamPreDispatch (int, string)</li>
					<li>hasParamScoring (string)</li>
					<li>hasParamVerbose (boolean, int)</li>
				</ul>
			</details>
			<details>
				<summary>CrossValidateMethod</summary>
				<ul>
					<li>hasParamCv (int, string)</li>
					<li>hasParamErrorScore (string)</li>
					<li>hasParamFitParams (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamParams (string)</li>
					<li>hasParamPreDispatch (int, string)</li>
					<li>hasParamReturnEstimator (boolean)</li>
					<li>hasParamReturnIndices (boolean)</li>
					<li>hasParamReturnTrainScore (boolean)</li>
					<li>hasParamScoring (string)</li>
					<li>hasParamVerbose (boolean, int)</li>
				</ul>
			</details>
			<details>
				<summary>DataSplittingMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>GroupKFoldMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
				</ul>
			</details>
			<details>
				<summary>GroupShuffleSplitMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamTestSize (float, int)</li>
					<li>hasParamTrainSize (float, int)</li>
				</ul>
			</details>
			<details>
				<summary>KFoldMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamShuffle (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>LearningCurveDisplayMethod</summary>
				<ul>
					<li>hasParamScoreName (string)</li>
					<li>hasParamTestScores (string)</li>
					<li>hasParamTrainScores (string)</li>
				</ul>
			</details>
			<details>
				<summary>LearningCurveMethod</summary>
				<ul>
					<li>hasParamCv (int, string)</li>
					<li>hasParamErrorScore (string)</li>
					<li>hasParamEstimator (string)</li>
					<li>hasParamExploitIncrementalLearning (boolean)</li>
					<li>hasParamFitParams (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamPreDispatch (int, string)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamReturnTimes (boolean)</li>
					<li>hasParamScoring (string)</li>
					<li>hasParamShuffle (boolean)</li>
					<li>hasParamVerbose (boolean, int)</li>
				</ul>
			</details>
			<details>
				<summary>LeavePGroupsOutMethod</summary>
				<ul>
					<li>hasParamNGroups (int)</li>
				</ul>
			</details>
			<details>
				<summary>LeavePOutMethod</summary>
				<ul>
					<li>hasParamP (float, int)</li>
				</ul>
			</details>
			<details>
				<summary>PermutationTestScoreMethod</summary>
				<ul>
					<li>hasParamCv (int, string)</li>
					<li>hasParamFitParams (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamNPermutations (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamScoring (string)</li>
					<li>hasParamVerbose (boolean, int)</li>
				</ul>
			</details>
			<details>
				<summary>PredefinedSplitMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>RepeatedKFoldMethod</summary>
				<ul>
					<li>hasParamNRepeats (int)</li>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
				</ul>
			</details>
			<details>
				<summary>RepeatedStratifiedKFoldMethod</summary>
				<ul>
					<li>hasParamNRepeats (int)</li>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
				</ul>
			</details>
			<details>
				<summary>ShuffleSplitMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamTestSize (float, int)</li>
					<li>hasParamTrainSize (float, int)</li>
				</ul>
			</details>
			<details>
				<summary>StratifiedGroupKFoldMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamShuffle (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>StratifiedKFoldMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamShuffle (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>StratifiedShuffleSplitMethod</summary>
				<ul>
					<li>hasParamNSplits (int)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamTestSize (float, int)</li>
					<li>hasParamTrainSize (float, int)</li>
				</ul>
			</details>
			<details>
				<summary>TimeSeriesSplitMethod</summary>
				<ul>
					<li>hasParamGap (int)</li>
					<li>hasParamMaxTrainSize (int)</li>
					<li>hasParamNSplits (int)</li>
					<li>hasParamTestSize (float, int)</li>
				</ul>
			</details>
			<details>
				<summary>TrainTestSplitMethod</summary>
				<ul>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamShuffle (boolean)</li>
					<li>hasParamStratify (string)</li>
					<li>hasParamTestSize (float, int)</li>
					<li>hasParamTrainSize (float, int)</li>
				</ul>
			</details>
			<details>
				<summary>ValidationCurveDisplayMethod</summary>
				<ul>
					<li>hasParamParamName (string)</li>
					<li>hasParamScoreName (string)</li>
					<li>hasParamTestScores (string)</li>
					<li>hasParamTrainScores (string)</li>
				</ul>
			</details>
			<details>
				<summary>ValidationCurveMethod</summary>
				<ul>
					<li>hasParamCv (int, string)</li>
					<li>hasParamErrorScore (string)</li>
					<li>hasParamEstimator (string)</li>
					<li>hasParamFitParams (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamParamName (string)</li>
					<li>hasParamPreDispatch (int, string)</li>
					<li>hasParamScoring (string)</li>
					<li>hasParamVerbose (boolean, int)</li>
				</ul>
			</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>PerformanceCalculation ☑️<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>Inputs</summary>
			<ul>
				<li>DataInPredictedY</li>
				<li>DataInRealY</li>
			</ul>
		</details>
		<details>
			<summary>Outputs</summary>
			<ul>
				<li>DataOutScore</li>
			</ul>
		</details>
		<details>
			<summary>Methods</summary>
			<ul>
			<details>
				<summary>AccuracyScoreMethod</summary>
				<ul>
					<li>hasParamNormalize (boolean, string)</li>
				</ul>
			</details>
			<details>
				<summary>AdjustedMutualInfoScoreMethod</summary>
				<ul>
					<li>hasParamAverageMethod (string)</li>
				</ul>
			</details>
			<details>
				<summary>AdjustedRandScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>AucMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>AveragePrecisionScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
				</ul>
			</details>
			<details>
				<summary>BalancedAccuracyScoreMethod</summary>
				<ul>
					<li>hasParamAdjusted (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>BrierScoreLossMethod</summary>
				<ul>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
				</ul>
			</details>
			<details>
				<summary>CalinskiHarabaszScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>CheckScoringMethod</summary>
				<ul>
					<li>hasParamAllowNone (boolean)</li>
					<li>hasParamScoring (string)</li>
				</ul>
			</details>
			<details>
				<summary>ClassLikelihoodRatiosMethod</summary>
				<ul>
					<li>hasParamRaiseWarning (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>ClassificationReportMethod</summary>
				<ul>
					<li>hasParamDigits (int)</li>
					<li>hasParamOutputDict (boolean)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>CohenKappaScoreMethod</summary>
				<ul>
					<li>hasParamWeights (string)</li>
				</ul>
			</details>
			<details>
				<summary>CompletenessScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>ConfusionMatrixMethod</summary>
				<ul>
					<li>hasParamNormalize (boolean, string)</li>
				</ul>
			</details>
			<details>
				<summary>ConsensusScoreMethod</summary>
				<ul>
					<li>hasParamA (string)</li>
					<li>hasParamB (string)</li>
					<li>hasParamSimilarity (string)</li>
				</ul>
			</details>
			<details>
				<summary>CoverageErrorMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>D2AbsoluteErrorScoreMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>D2PinballScoreMethod</summary>
				<ul>
					<li>hasParamAlpha (float, int, string)</li>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>D2TweedieScoreMethod</summary>
				<ul>
					<li>hasParamPower (float)</li>
				</ul>
			</details>
			<details>
				<summary>DaviesBouldinScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>DcgScoreMethod</summary>
				<ul>
					<li>hasParamIgnoreTies (boolean)</li>
					<li>hasParamK (int)</li>
					<li>hasParamLogBase (float)</li>
				</ul>
			</details>
			<details>
				<summary>DetCurveMethod</summary>
				<ul>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
				</ul>
			</details>
			<details>
				<summary>EuclideanDistancesMethod</summary>
				<ul>
					<li>hasParamSquared (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>ExplainedVarianceScoreMethod</summary>
				<ul>
					<li>hasParamForceFinite (boolean)</li>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>F1ScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>FbetaScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamBeta (float)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>FowlkesMallowsScoreMethod</summary>
				<ul>
					<li>hasParamSparse (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>GetScorerMethod</summary>
				<ul>
					<li>hasParamScoring (string)</li>
				</ul>
			</details>
			<details>
				<summary>GetScorerNamesMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>HammingLossMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>HingeLossMethod</summary>
				<ul>
					<li>hasParamPredDecision (string)</li>
				</ul>
			</details>
			<details>
				<summary>HomogeneityCompletenessVMeasureMethod</summary>
				<ul>
					<li>hasParamBeta (float)</li>
				</ul>
			</details>
			<details>
				<summary>HomogeneityScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>JaccardScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>LabelRankingAveragePrecisionScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>LabelRankingLossMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>LogLossMethod</summary>
				<ul>
					<li>hasParamEps (float)</li>
					<li>hasParamNormalize (boolean, string)</li>
				</ul>
			</details>
			<details>
				<summary>MakeScorerMethod</summary>
				<ul>
					<li>hasParamGreaterIsBetter (boolean)</li>
					<li>hasParamNeedsProba (boolean)</li>
					<li>hasParamNeedsThreshold (boolean)</li>
					<li>hasParamResponseMethod (string)</li>
					<li>hasParamScoreFunc (string)</li>
				</ul>
			</details>
			<details>
				<summary>MatthewsCorrcoefMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>MaxErrorMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>MeanAbsoluteErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>MeanAbsolutePercentageErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>MeanGammaDevianceMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>MeanPinballLossMethod</summary>
				<ul>
					<li>hasParamAlpha (float, int, string)</li>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>MeanPoissonDevianceMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>MeanSquaredErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
					<li>hasParamSquared (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>MeanSquaredLogErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
					<li>hasParamSquared (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>MeanTweedieDevianceMethod</summary>
				<ul>
					<li>hasParamPower (float)</li>
				</ul>
			</details>
			<details>
				<summary>MedianAbsoluteErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>MultilabelConfusionMatrixMethod</summary>
				<ul>
					<li>hasParamSamplewise (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>MutualInfoScoreMethod</summary>
				<ul>
					<li>hasParamContingency (string)</li>
				</ul>
			</details>
			<details>
				<summary>NanEuclideanDistancesMethod</summary>
				<ul>
					<li>hasParamCopy (boolean)</li>
					<li>hasParamMissingValues (float, int, string)</li>
					<li>hasParamSquared (boolean)</li>
				</ul>
			</details>
			<details>
				<summary>NdcgScoreMethod</summary>
				<ul>
					<li>hasParamIgnoreTies (boolean)</li>
					<li>hasParamK (int)</li>
				</ul>
			</details>
			<details>
				<summary>NormalizedMutualInfoScoreMethod</summary>
				<ul>
					<li>hasParamAverageMethod (string)</li>
				</ul>
			</details>
			<details>
				<summary>PairConfusionMatrixMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>PairwiseDistancesArgminMethod</summary>
				<ul>
					<li>hasParamAxis (int)</li>
					<li>hasParamMetric (string)</li>
					<li>hasParamMetricKwargs (string)</li>
				</ul>
			</details>
			<details>
				<summary>PairwiseDistancesArgminMinMethod</summary>
				<ul>
					<li>hasParamAxis (int)</li>
					<li>hasParamMetric (string)</li>
					<li>hasParamMetricKwargs (string)</li>
				</ul>
			</details>
			<details>
				<summary>PairwiseDistancesChunkedMethod</summary>
				<ul>
					<li>hasParamMetric (string)</li>
					<li>hasParamNJobs (int, string)</li>
					<li>hasParamReduceFunc (string)</li>
					<li>hasParamWorkingMemory (float)</li>
				</ul>
			</details>
			<details>
				<summary>PairwiseDistancesMethod</summary>
				<ul>
					<li>hasParamForceAllFinite (boolean)</li>
					<li>hasParamMetric (string)</li>
					<li>hasParamNJobs (int, string)</li>
				</ul>
			</details>
			<details>
				<summary>PairwiseKernelsMethod</summary>
				<ul>
					<li>hasParamFilterParams (boolean)</li>
					<li>hasParamMetric (string)</li>
					<li>hasParamNJobs (int, string)</li>
				</ul>
			</details>
			<details>
				<summary>PerformanceCalculationMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>PrecisionRecallCurveMethod</summary>
				<ul>
					<li>hasParamDropIntermediate (boolean)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
				</ul>
			</details>
			<details>
				<summary>PrecisionRecallFscoreSupportMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamBeta (float)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
					<li>hasParamWarnFor (string)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>PrecisionScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>R2ScoreMethod</summary>
				<ul>
					<li>hasParamForceFinite (boolean)</li>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>RandScoreMethod</summary>
				<ul>No parameters</ul>
			</details>
			<details>
				<summary>RecallScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
					<li>hasParamZeroDivision (string)</li>
				</ul>
			</details>
			<details>
				<summary>RocAucScoreMethod</summary>
				<ul>
					<li>hasParamAverage (boolean, int, string)</li>
					<li>hasParamMultiClass (string)</li>
				</ul>
			</details>
			<details>
				<summary>RocCurveMethod</summary>
				<ul>
					<li>hasParamDropIntermediate (boolean)</li>
					<li>hasParamPosLabel (boolean, float, int, string)</li>
				</ul>
			</details>
			<details>
				<summary>RootMeanSquaredErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>RootMeanSquaredLogErrorMethod</summary>
				<ul>
					<li>hasParamMultioutput (string)</li>
				</ul>
			</details>
			<details>
				<summary>SilhouetteSamplesMethod</summary>
				<ul>
					<li>hasParamMetric (string)</li>
				</ul>
			</details>
			<details>
				<summary>SilhouetteScoreMethod</summary>
				<ul>
					<li>hasParamMetric (string)</li>
					<li>hasParamRandomState (int, string)</li>
					<li>hasParamSampleSize (int)</li>
				</ul>
			</details>
			<details>
				<summary>TopKAccuracyScoreMethod</summary>
				<ul>
					<li>hasParamK (int)</li>
					<li>hasParamNormalize (boolean, string)</li>
				</ul>
			</details>
			<details>
				<summary>VMeasureScoreMethod</summary>
				<ul>
					<li>hasParamBeta (float)</li>
				</ul>
			</details>
			<details>
				<summary>ZeroOneLossMethod</summary>
				<ul>
					<li>hasParamNormalize (boolean, string)</li>
				</ul>
			</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>Test ☑️<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>Inputs</summary>
			<ul>
				<li>DataInTestModel</li>
				<li>DataInTestX</li>
			</ul>
		</details>
		<details>
			<summary>Outputs</summary>
			<ul>
				<li>DataOutPredictedValueTest</li>
			</ul>
		</details>
		<details>
			<summary>Methods</summary>
			<ul>
			<details>
				<summary>TestMethod</summary>
				<ul>No parameters</ul>
			</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>Transform ☑️<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>ml</code></span></summary>
	<ul>
		<details>
			<summary>Inputs</summary>
			<ul>
				<li>DataInToTransform</li>
				<li>DataInTransformer</li>
			</ul>
		</details>
		<details>
			<summary>Outputs</summary>
			<ul>
				<li>DataOutTransformed</li>
			</ul>
		</details>
		<details>
			<summary>Methods</summary>
			<ul>
			<details>
				<summary>TransformMethod</summary>
				<ul>No parameters</ul>
			</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>StatisticCalculation 📜<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>stats</code></span></summary>
	<ul>
		<details>
			<summary>CentralTendencyMeasure ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>AverageMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamReturned (boolean)</li>
							<li>hasParamWeights (string)</li>
						</ul>
					</details>
					<details>
						<summary>MeanMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamWhere (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>MedianMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamOverwriteInput (boolean)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>DependencyMeasure ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>CorrcoefMethod</summary>
						<ul>
							<li>hasParamBias (boolean, string)</li>
							<li>hasParamDdof (int, string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamRowvar (boolean)</li>
							<li>hasParamX (string)</li>
							<li>hasParamY (string)</li>
						</ul>
					</details>
					<details>
						<summary>CovMethod</summary>
						<ul>
							<li>hasParamAweights (string)</li>
							<li>hasParamBias (boolean, string)</li>
							<li>hasParamDdof (int, string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamFweights (int, string)</li>
							<li>hasParamM (string)</li>
							<li>hasParamRowvar (boolean)</li>
							<li>hasParamY (string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>DispersionMeasure ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>StdMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamDdof (int, string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamWhere (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>VarMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamDdof (int, string)</li>
							<li>hasParamDtype (string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamWhere (boolean)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>PositionMeasure ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>PercentileMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamInterpolation (string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamMethod (string)</li>
							<li>hasParamOverwriteInput (boolean)</li>
							<li>hasParamQ (float)</li>
						</ul>
					</details>
					<details>
						<summary>QuantileMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamInterpolation (string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamMethod (string)</li>
							<li>hasParamOverwriteInput (boolean)</li>
							<li>hasParamQ (float)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>ShapeMeasure ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
					<ul>
						<li>DataOutStatisticCalculation</li>
					</ul>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>KurtosisMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamBias (boolean, string)</li>
							<li>hasParamFisher (boolean)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamNanPolicy (string)</li>
						</ul>
					</details>
					<details>
						<summary>PtpMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamKeepdims (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>SkewMethod</summary>
						<ul>
							<li>hasParamAxis (int, string)</li>
							<li>hasParamBias (boolean, string)</li>
							<li>hasParamKeepdims (boolean)</li>
							<li>hasParamNanPolicy (string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>Plotting 📜<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>visu</code></span></summary>
	<ul>
		<details>
			<summary>AreaPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>FillBetweenMethod</summary>
						<ul>
							<li>hasParamInterpolate (boolean)</li>
							<li>hasParamStep (string)</li>
							<li>hasParamWhere (string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamY1 (float, string)</li>
							<li>hasParamY2 (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>FillMethod</summary>
						<ul>No parameters</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>BarPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>BarMethod</summary>
						<ul>
							<li>hasParamAlign (string)</li>
							<li>hasParamBottom (float, string)</li>
							<li>hasParamHeight (float, string)</li>
							<li>hasParamWidth (float, string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>BarhMethod</summary>
						<ul>
							<li>hasParamAlign (string)</li>
							<li>hasParamHeight (float, string)</li>
							<li>hasParamLeft (float, string)</li>
							<li>hasParamWidth (float, string)</li>
							<li>hasParamY (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>BoxPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>BoxplotMethod</summary>
						<ul>
							<li>hasParamAutorange (boolean)</li>
							<li>hasParamBootstrap (int, string)</li>
							<li>hasParamBoxprops (string)</li>
							<li>hasParamCapprops (string)</li>
							<li>hasParamCapwidths (float, string)</li>
							<li>hasParamConfIntervals (string)</li>
							<li>hasParamFlierprops (string)</li>
							<li>hasParamLabels (string)</li>
							<li>hasParamManageTicks (boolean)</li>
							<li>hasParamMeanline (boolean, string)</li>
							<li>hasParamMeanprops (string)</li>
							<li>hasParamMedianprops (string)</li>
							<li>hasParamNotch (boolean, string)</li>
							<li>hasParamPatchArtist (boolean, string)</li>
							<li>hasParamPositions (string)</li>
							<li>hasParamShowbox (boolean, string)</li>
							<li>hasParamShowcaps (boolean, string)</li>
							<li>hasParamShowfliers (boolean, string)</li>
							<li>hasParamShowmeans (boolean, string)</li>
							<li>hasParamSym (string)</li>
							<li>hasParamUsermedians (string)</li>
							<li>hasParamVert (boolean, string)</li>
							<li>hasParamWhis (float, string)</li>
							<li>hasParamWhiskerprops (string)</li>
							<li>hasParamWidths (float, string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamZorder (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>ContourPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>ContourMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>ContourfMethod</summary>
						<ul>No parameters</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>ErrorBarPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>ErrorbarMethod</summary>
						<ul>
							<li>hasParamBarsabove (boolean)</li>
							<li>hasParamCapsize (float, string)</li>
							<li>hasParamCapthick (float, string)</li>
							<li>hasParamEcolor (string)</li>
							<li>hasParamElinewidth (float, string)</li>
							<li>hasParamErrorevery (int, string)</li>
							<li>hasParamFmt (string)</li>
							<li>hasParamLolims (boolean, string)</li>
							<li>hasParamUplims (boolean, string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamXerr (float, string)</li>
							<li>hasParamXlolims (boolean, string)</li>
							<li>hasParamXuplims (boolean, string)</li>
							<li>hasParamY (float, string)</li>
							<li>hasParamYerr (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>Histogram ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>HexbinMethod</summary>
						<ul>
							<li>hasParamAlpha (float, string)</li>
							<li>hasParamBins (int, string)</li>
							<li>hasParamC (string)</li>
							<li>hasParamCmap (string)</li>
							<li>hasParamEdgecolors (string)</li>
							<li>hasParamExtent (string)</li>
							<li>hasParamGridsize (int, string)</li>
							<li>hasParamLinewidths (float, string)</li>
							<li>hasParamMarginals (boolean)</li>
							<li>hasParamMincnt (int, string)</li>
							<li>hasParamNorm (string)</li>
							<li>hasParamReduceCFunction (string)</li>
							<li>hasParamVmax (float, string)</li>
							<li>hasParamVmin (float, string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamXscale (string)</li>
							<li>hasParamY (float, string)</li>
							<li>hasParamYscale (string)</li>
						</ul>
					</details>
					<details>
						<summary>Hist2dMethod</summary>
						<ul>
							<li>hasParamBins (int, string)</li>
							<li>hasParamCmax (float, string)</li>
							<li>hasParamCmin (float, string)</li>
							<li>hasParamDensity (boolean, float)</li>
							<li>hasParamRange (string)</li>
							<li>hasParamWeights (string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamY (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>HistMethod</summary>
						<ul>
							<li>hasParamAlign (string)</li>
							<li>hasParamBins (int, string)</li>
							<li>hasParamBottom (float, string)</li>
							<li>hasParamColor (string)</li>
							<li>hasParamCumulative (boolean, float)</li>
							<li>hasParamDensity (boolean, float)</li>
							<li>hasParamHisttype (string)</li>
							<li>hasParamLabel (string)</li>
							<li>hasParamLog (boolean)</li>
							<li>hasParamOrientation (string)</li>
							<li>hasParamRange (string)</li>
							<li>hasParamRwidth (float, string)</li>
							<li>hasParamStacked (boolean)</li>
							<li>hasParamWeights (string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>ImagePlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>ImshowMethod</summary>
						<ul>
							<li>hasParamAlpha (float, string)</li>
							<li>hasParamAspect (float, string)</li>
							<li>hasParamCmap (string)</li>
							<li>hasParamExtent (string)</li>
							<li>hasParamFilternorm (boolean)</li>
							<li>hasParamFilterrad (float)</li>
							<li>hasParamInterpolation (string)</li>
							<li>hasParamInterpolationStage (string)</li>
							<li>hasParamNorm (string)</li>
							<li>hasParamOrigin (string)</li>
							<li>hasParamResample (boolean, string)</li>
							<li>hasParamUrl (string)</li>
							<li>hasParamVmax (float, string)</li>
							<li>hasParamVmin (float, string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>PcolorMethod</summary>
						<ul>
							<li>hasParamAlpha (float, string)</li>
							<li>hasParamArgs (float, string)</li>
							<li>hasParamCmap (string)</li>
							<li>hasParamNorm (string)</li>
							<li>hasParamShading (string)</li>
							<li>hasParamVmax (float, string)</li>
							<li>hasParamVmin (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>PcolormeshMethod</summary>
						<ul>
							<li>hasParamAlpha (float, string)</li>
							<li>hasParamAntialiased (boolean)</li>
							<li>hasParamArgs (float, string)</li>
							<li>hasParamCmap (string)</li>
							<li>hasParamNorm (string)</li>
							<li>hasParamShading (string)</li>
							<li>hasParamVmax (float, string)</li>
							<li>hasParamVmin (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>LinePlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>AcorrMethod</summary>
						<ul>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>AngleSpectrumMethod</summary>
						<ul>
							<li>hasParamFc (int, string)</li>
							<li>hasParamFs (float, string)</li>
							<li>hasParamPadTo (int, string)</li>
							<li>hasParamSides (string)</li>
							<li>hasParamWindow (string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>CohereMethod</summary>
						<ul>
							<li>hasParamDetrend (string)</li>
							<li>hasParamFc (int, string)</li>
							<li>hasParamFs (float, string)</li>
							<li>hasParamNfft (int)</li>
							<li>hasParamNoverlap (int)</li>
							<li>hasParamPadTo (int, string)</li>
							<li>hasParamScaleByFreq (boolean, string)</li>
							<li>hasParamSides (string)</li>
							<li>hasParamWindow (string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamY (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>LoglogMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>MagnitudeSpectrumMethod</summary>
						<ul>
							<li>hasParamFc (int, string)</li>
							<li>hasParamFs (float, string)</li>
							<li>hasParamPadTo (int, string)</li>
							<li>hasParamScale (string)</li>
							<li>hasParamSides (string)</li>
							<li>hasParamWindow (string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>PhaseSpectrumMethod</summary>
						<ul>
							<li>hasParamFc (int, string)</li>
							<li>hasParamFs (float, string)</li>
							<li>hasParamPadTo (int, string)</li>
							<li>hasParamSides (string)</li>
							<li>hasParamWindow (string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>PlotMethod</summary>
						<ul>
							<li>hasParamArgs (float, string)</li>
							<li>hasParamScalex (boolean)</li>
							<li>hasParamScaley (boolean)</li>
						</ul>
					</details>
					<details>
						<summary>SemilogxMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>SemilogyMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>StackplotMethod</summary>
						<ul>
							<li>hasParamBaseline (string)</li>
							<li>hasParamColors (string)</li>
							<li>hasParamLabels (string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>StemMethod</summary>
						<ul>
							<li>hasParamArgs (float, string)</li>
							<li>hasParamBasefmt (string)</li>
							<li>hasParamBottom (float, string)</li>
							<li>hasParamLabel (string)</li>
							<li>hasParamLinefmt (string)</li>
							<li>hasParamMarkerfmt (string)</li>
							<li>hasParamOrientation (string)</li>
						</ul>
					</details>
					<details>
						<summary>StepMethod</summary>
						<ul>
							<li>hasParamWhere (string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamY (float, string)</li>
						</ul>
					</details>
					<details>
						<summary>XcorrMethod</summary>
						<ul>
							<li>hasParamDetrend (string)</li>
							<li>hasParamMaxlags (int)</li>
							<li>hasParamNormed (boolean)</li>
							<li>hasParamUsevlines (boolean)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamY (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>PieChart ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>PieMethod</summary>
						<ul>
							<li>hasParamAutopct (string)</li>
							<li>hasParamCenter (string)</li>
							<li>hasParamColors (string)</li>
							<li>hasParamCounterclock (boolean)</li>
							<li>hasParamExplode (string)</li>
							<li>hasParamFrame (boolean)</li>
							<li>hasParamHatch (string)</li>
							<li>hasParamLabeldistance (float, string)</li>
							<li>hasParamLabels (string)</li>
							<li>hasParamNormalize (boolean)</li>
							<li>hasParamPctdistance (float)</li>
							<li>hasParamRadius (float)</li>
							<li>hasParamRotatelabels (boolean)</li>
							<li>hasParamShadow (boolean)</li>
							<li>hasParamStartangle (float)</li>
							<li>hasParamTextprops (string)</li>
							<li>hasParamWedgeprops (string)</li>
							<li>hasParamX (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>PolarPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>PolarMethod</summary>
						<ul>No parameters</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>ScatterPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>ScatterMethod</summary>
						<ul>
							<li>hasParamAlpha (float, string)</li>
							<li>hasParamC (string)</li>
							<li>hasParamCmap (string)</li>
							<li>hasParamEdgecolors (string)</li>
							<li>hasParamLinewidths (float, string)</li>
							<li>hasParamMarker (string)</li>
							<li>hasParamNorm (string)</li>
							<li>hasParamPlotnonfinite (boolean)</li>
							<li>hasParamS (float, string)</li>
							<li>hasParamVmax (float, string)</li>
							<li>hasParamVmin (float, string)</li>
							<li>hasParamX (float, string)</li>
							<li>hasParamY (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>VectorField ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>QuiverMethod</summary>
						<ul>No parameters</ul>
					</details>
					<details>
						<summary>StreamplotMethod</summary>
						<ul>
							<li>hasParamArrowsize (float)</li>
							<li>hasParamArrowstyle (string)</li>
							<li>hasParamBrokenStreamlines (string)</li>
							<li>hasParamColor (string)</li>
							<li>hasParamDensity (boolean, float)</li>
							<li>hasParamIntegrationDirection (string)</li>
							<li>hasParamLinewidth (float, string)</li>
							<li>hasParamMaxlength (float)</li>
							<li>hasParamMinlength (float)</li>
							<li>hasParamStartPoints (string)</li>
							<li>hasParamZorder (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
		<details>
			<summary>ViolinPlotting ☑️</summary>
			<ul>
				<details>
					<summary>Inputs</summary>
					<ul>
						<li>DataInToPlot</li>
					</ul>
				</details>
				<details>
					<summary>Outputs</summary>
				</details>
				<details>
					<summary>Methods</summary>
					<ul>
					<details>
						<summary>ViolinplotMethod</summary>
						<ul>
							<li>hasParamBwMethod (float, string)</li>
							<li>hasParamDataset (string)</li>
							<li>hasParamPoints (int)</li>
							<li>hasParamPositions (string)</li>
							<li>hasParamQuantiles (string)</li>
							<li>hasParamShowextrema (boolean)</li>
							<li>hasParamShowmeans (boolean, string)</li>
							<li>hasParamShowmedians (boolean)</li>
							<li>hasParamVert (boolean, string)</li>
							<li>hasParamWidths (float, string)</li>
						</ul>
					</details>
					</ul>
				</details>
			</ul>
		</details>
	</ul>
</details>
<details>
	<summary>CanvasCreation ☑️<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>visu</code></span></summary>
	<ul>
		<details>
			<summary>Inputs</summary>
		</details>
		<details>
			<summary>Outputs</summary>
		</details>
		<details>
			<summary>Methods</summary>
			<ul>
			<details>
				<summary>CanvasMethod</summary>
				<ul>
					<li>hasParamFigureSize (string)</li>
					<li>hasParamLayout (string)</li>
				</ul>
			</details>
			</ul>
		</details>
	</ul>
</details>
