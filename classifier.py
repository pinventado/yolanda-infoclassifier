from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.externals import joblib
from os import path
import numpy as np, traceback, sys
from gevent.coros import Semaphore

class ReliefClassifier:
	def __init__(self, batch_size = 5, timeout = 300):
		self.batch_size = batch_size
		self.timeout = timeout
		self.base_dir = 'model'
		self.vect_file = 'hash.vec'
		if  path.isfile(path.join(self.base_dir, self.vect_file)):
			self.vectorizer = joblib.load(path.join(self.base_dir, self.vect_file))
		else:
			self.vectorizer = HashingVectorizer(ngram_range=(1,3), stop_words='english')

		self.classifier_file = 'aidclassifier.model'
		if  path.isfile(path.join(self.base_dir, self.classifier_file)):
			self.classifier = joblib.load(path.join(self.base_dir, self.classifier_file))			
			self.first = None
		else:
			self.classifier = SGDClassifier()
			self.first = True
		
		self.doc_set = []
		self.label_set = []
		self.doc_count = 0
		self.lock = Semaphore()

	def train(self, doc_set, label_set):
		sys.stdout.write("hashing\n")
		print doc_set
		print label_set
		train = np.array(doc_set)
		vectorized_train = self.vectorizer.fit_transform(train)
		sys.stdout.write("training\n")
		sys.stdout.flush()
		#print vectorized_train
		try:
			self.classifier.partial_fit(vectorized_train, label_set, ['A','NA'])
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
			sys.stdout.flush()


	def predict(self, doc_set):
		if self.first == None:
			test = np.array(doc_set)
			vectorized_test = self.vectorizer.fit_transform(test)
			with self.lock:
				sys.stdout.write("predicting\n")
				sys.stdout.flush()
				#print vectorized_test		
				prediction = self.classifier.predict(vectorized_test)
			return prediction
		else:
			return -1

	def addDocument(self, doc, label):
		self.doc_set.append(doc)
		self.label_set.append(str(label))
		self.doc_count+=1					
		if self.doc_count == self.batch_size:
			sys.stdout.write("batch reached\n")
			sys.stdout.flush()
			self.train(self.doc_set, self.label_set)
			with self.lock:
				joblib.dump(self.vectorizer, path.join(self.base_dir, self.vect_file))
				joblib.dump(self.classifier, path.join(self.base_dir, self.classifier_file))
				self.first = None
			self.doc_set = []
			self.label_set = []
			self.doc_count = 0

